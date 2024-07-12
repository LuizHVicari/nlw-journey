import { View, Text, Image, Keyboard, Alert } from 'react-native'
import { Input } from '@/components/input'
import { MapPin, Calendar as IconCalendar, Settings2, UserRoundPlus, ArrowRight, AtSign } from 'lucide-react-native'
import { colors } from '@/styles/colors'
import { Button } from '@/components/button'
import { Fragment, useEffect, useState } from 'react'
import { Modal } from '@/components/modal'
import { Calendar } from '@/components/calendar'
import { calendarUtils, DatesSelected } from '@/utils/calendarUtils'
import { DateData } from 'react-native-calendars'
import dayjs from 'dayjs'
import '@/utils/dayjsLocaleConfig'
import { GuestEmail } from '@/components/email'
import { validateInput } from '@/utils/validateInput'
import { get, save, remove } from '@/storage/trip'
import { router } from 'expo-router'
import { tripServer } from '@/server/trip-server'
import { Loading } from '@/components/loading'

enum StepForm {
  TRIP_DETAILS = 1,
  ADD_EMAIL = 2,
}

enum MODAL {
  NONE = 0,
  CALENDAR = 1,
  GUESTS = 2,
}

export default function Index() {
  const [isGettingTrip, setIsGettingTrip ] = useState(true)
  const [stepForm, setStepForm] = useState(StepForm.TRIP_DETAILS)
  const [showModal, setShowModal] = useState(MODAL.NONE)
  const [selectedDates, setSelectedDates] = useState({} as DatesSelected)
  const [destination, setDestination] = useState('')
  const [emailToInvite, setEmailToInvite] = useState('')
  const [emailsToInvite, setEmailsToInvite] = useState<string[]>([])
  const [isCreatingTrip, setIsCreatingTrip] = useState(false)

  async function saveTrip(tripId: string) {
    try {
      await save(tripId)
      console.log(tripId)
      router.navigate('/trip/' + tripId)
    } catch (error) {
      Alert.alert(
        'Salvar viagem',
        'Não foi possível salvar o id da viagem no dispositivo'
      )
      console.log(error)
    }
  }


  async function createTrip() {
    try {
      setIsCreatingTrip(true)

      const newTrip = await tripServer.create({
        destination,
        starts_at: dayjs(selectedDates.startsAt?.dateString).toString(),
        ends_at: dayjs(selectedDates.endsAt?.dateString).toString(),
        emails_to_invite: emailsToInvite
      })
      Alert.alert(
        'Nova viagem',
        'Viagem criada com sucesso!',
        [{
          text: 'Ok, continuar',
          onPress: () => saveTrip(newTrip.tripId)
        }]
      )
      
    } catch (error) {
      console.log(error)
      setIsCreatingTrip(false)
    }
  }


  function handleSelectedDate(selectedDay: DateData) {
    const dates = calendarUtils.orderStartsAtAndEndsAt({
      startsAt: selectedDates.startsAt,
      endsAt: selectedDates.endsAt,
      selectedDay,
    })
    setSelectedDates(dates)
  }

  function handleAddEmail() {
    if(!validateInput.email(emailToInvite)) {
      return Alert.alert(
        'Convidado',
        'E-mail invalido'
      )
    }

    const emailAlreadyExists = emailsToInvite.find((email) => email === emailToInvite)
    if (emailAlreadyExists) {
      return Alert.alert(
        'Convidado',
        'E-mail já adicionado'
      )
    }

    setEmailsToInvite((prevState) => [...prevState, emailToInvite])
    setEmailToInvite('')

  }


  function handleRemoveEmail(emailToRemove: string) {
    setEmailsToInvite((prevState) =>
      prevState.filter((email) => email !== emailToRemove)
  )
  }

  function handleNextStepForm() {
    if (destination.trim().length === 0 || !selectedDates.startsAt || !selectedDates.endsAt) {
      return Alert.alert(
        'Detalhes da viagem',
        'Preencha todas as informações da viagem para seguir'
      )
    }

    if (destination.length < 4) {
      return Alert.alert(
        'Detalhes da viagem',
        'O destino deve ter pelo menos 4 caracteres'
      )
    }

    if(stepForm === StepForm.TRIP_DETAILS) {
      return setStepForm(StepForm.ADD_EMAIL)
    }

    Alert.alert(
      'Nova viagem',
      'Confirmar viagem?',
      [
        {
          text: 'Não',
          style: 'cancel'
        },
        {
          text: 'Sim',
          onPress: createTrip
        }
      ]
    )
  }

  async function getTrip() {
    try {
      const tripId = await get()
      console.log(tripId)
      if (!tripId) {
        return setIsGettingTrip(false)
      }

      const trip = await tripServer.getById(tripId)

      if (trip) {
        console.log(trip)
        return router.navigate('/trip/' + trip.id)
      }
      
    } catch (error) {
      setIsGettingTrip(false)
      console.log(error)
      

    }
  }
    useEffect(() => {
      getTrip()
    }, [])

    if(isGettingTrip) {
      return <Loading/>
    }
  

  return (
    <View className='flex-1 items-center justify-center px-5'>
      <Image 
        source={require("@/assets/logo.png")} 
        className='h-8' 
        resizeMode='contain'
      />

      <Image
        source={require('@/assets/bg.png')}
        className='absolute'
      />

      <Text 
        className='text-zinc-400 font-regular text-center text-lg mt-3'
      >
        Convide seus amigos e planeje sua{'\n'}próxima viagem
      </Text>

      <View
        className='w-full bg-zinc-900 p-4 rounded-xl my-8 border border-l-zinc-800'
      >
        <Input>
        <MapPin color={colors.zinc[400]} size={20}/>
          <Input.Field
            placeholder='Para onde?'
            editable={stepForm === StepForm.TRIP_DETAILS}
            value={destination}
            onChangeText={setDestination}
          />
        </Input>

        <Input>
        <IconCalendar color={colors.zinc[400]} size={20}/>
          <Input.Field
            placeholder='Quando?'
            editable={stepForm === StepForm.TRIP_DETAILS}
            onFocus={() => Keyboard.dismiss()}
            showSoftInputOnFocus={false}
            onPressIn={() => {stepForm === StepForm.TRIP_DETAILS && setShowModal(MODAL.CALENDAR)}}
            value={selectedDates.formatDatesInText}
          />
        </Input>

        {stepForm == StepForm.ADD_EMAIL && 
        <Fragment>

          <View className='border-b py-3 border-zinc-800'>
            <Button variant='secondary' isLoading={false} onPress={() => setStepForm(StepForm.TRIP_DETAILS)}>
              <Button.Title>Alterar local/data</Button.Title>
              <Settings2 color={colors.zinc[200]} size={20}/>
            </Button>
          </View>

          <Input>
          <UserRoundPlus color={colors.zinc[400]} size={20}/>
            <Input.Field
              placeholder='Quem estará na viagem?'
              autoCorrect={false}
              value = {
                emailsToInvite.length > 0 
                ? `${emailsToInvite.length} pessoa(s) convidada(s)`
                : ""
              }
              onPressIn={() => {
                Keyboard.dismiss()
                setShowModal(MODAL.GUESTS)
              }}
              showSoftInputOnFocus={false}
            />
          </Input>

        </Fragment>
        
        }

        <Button 
          onPress={handleNextStepForm}
          isLoading={isCreatingTrip}  
        >
          <Button.Title>
            {
              stepForm == StepForm.TRIP_DETAILS
               ? 'Continuar'
               : 'Confirmar Viagem'
            }
            
            
          </Button.Title>
          <ArrowRight color={colors.lime[950]} size={20}/>
        </Button>

        </View>

      <Text
        className='text-zinc-500 font-regular text-center text-base'
      >
        Ao planejar sua viagem com a plann.er você automaticamente concorda com nossos{' '}
        <Text className='text-zinc-300 underline'>  
          termos de uso e políticas de privacidade.
        </Text>
      </Text>


      <Modal
        title="Selecionar datas"
        subtitle='Selecione a data de ida e volta da viagem'
        visible={showModal == MODAL.CALENDAR}
        onClose={() => {setShowModal(MODAL.NONE)}}
      >

        <View
          className='gap-4 mt-4'
        >
          <Calendar
            onDayPress={handleSelectedDate}
            markedDates={selectedDates.dates}
            minDate={dayjs().toISOString()}
          />
          <Button
            onPress={() => setShowModal(MODAL.NONE)}
          >
            <Button.Title>
              Confirmar
            </Button.Title>
          </Button>
        </View>
      </Modal>

      <Modal
        title='Selecionar convidados'
        subtitle='Os convidados irão receber emails para confirmar a participação na viagem.'
        visible={showModal === MODAL.GUESTS}
        onClose={() => setShowModal(MODAL.NONE)}
      >


        <View
          className='mt-2 flex-wrap gap-2 border-b border-l-zinc-800 py-5'
        >{
          emailsToInvite.length > 0 ? (
            emailsToInvite.map((email) => (
              <GuestEmail
                key={email}
                email={email}
                onRemove={() => {handleRemoveEmail(email)}}
              />
            ))
          )
          : <Text className='text-zinc-600 text-base font-regular'>Nenhum e-mail adicionado </Text>
        }
        </View>

        <View
          className='gap-24 mt-4'
        >
          <Input variant='secondary'>
            <AtSign color={colors.zinc[400]} size={20}/>
            <Input.Field
              placeholder='Digite o email do convidado'
              keyboardType='email-address'
              onChangeText={(text) => setEmailToInvite(text.toLowerCase())}
              value={emailToInvite}
              returnKeyType='send'
              onSubmitEditing={handleAddEmail}
            />
          </Input>
          <Button onPress={handleAddEmail}>
            <Button.Title>Convidar</Button.Title>
          </Button>

        </View>



      </Modal>

    </View>

  )
}