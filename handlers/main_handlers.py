from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards import order_n_cancel_kb, cancel_kb, make_offer_kb
from forms import Offer
import requests
router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Для начала работы нажмите кнопку "Сделать заказ".', reply_markup=make_offer_kb)


@router.message(F.text == 'Сделать заказ')
async def get_offer(message: Message, state: FSMContext):
    await message.answer('Введите id желаемого товара')
    await state.set_state(Offer.id)


@router.message(Offer.id)
async def hello(message: Message, state: FSMContext):
    global prod_id
    try:
        prod_id = message.text
        await state.update_data(id=prod_id)
        data = requests.get(f'http://127.0.0.1:8000/take_from_db/{prod_id}').json()
        name = data['name']
        price = data['price']
        desc = data['description']
        await message.answer(f'Название товара: {name}\nЦена: {price}\nОписание: {desc}\n\nОформить заказ?',
                               reply_markup=order_n_cancel_kb)
        await state.set_state(Offer.is_confirmed)
    except:
        await message.answer('Такого товара не существует. Введите id еще раз')
        await state.set_state(Offer.id)


@router.message(Offer.is_confirmed)
async def confirm_offer(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Введите id другого товара')
        await state.set_state(Offer.id)
    elif message.text == 'Заказать':
        await state.update_data(is_confirmed=True)
        await message.answer('Введите адрес доставки\n!Вы можете нажать кнопку "Отмена" для выбора другого товара!',
                                reply_markup=cancel_kb)
        await state.set_state(Offer.address)
    else:
        await message.answer('Для продолжения нажмите либо "Заказать" либо "Отмена"')
        await state.set_state(Offer.is_confirmed)


@router.message(Offer.address)
async def get_address(message: Message, state: FSMContext):
    if message.text == 'Отмена':
        await message.answer('Хорошо. Введите id другого товара')
        await state.set_state(Offer.id)
    else:
        address = message.text
        await state.update_data(address=address)
        user_id = message.from_user.id
        offer_id = requests.post(f'http://127.0.0.1:8000/put_address_in_db?address={address}&prod_id={prod_id}&user_id={user_id}').text
        await message.answer(f'Ваш заказ успешно зарегистрирован. ID товара: {prod_id}, '
                                          f'адрес доставки: {address}, номер заказа: {offer_id}.', reply_markup=make_offer_kb)
        all_data = await state.get_data()
        print(all_data.get('id'), all_data.get('is_confirmed'), all_data.get('address'))
