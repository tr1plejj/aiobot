from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from keyboards import order_n_cancel_kb, cancel_kb, make_offer_kb
from forms import Offer
import requests
router = Router()
main_api_url = 'http://127.0.0.1:8000'


@router.message(CommandStart())
async def start(message: Message):
    await message.answer('Для начала работы нажмите кнопку "Сделать заказ".', reply_markup=make_offer_kb)


@router.message(F.text == 'Сделать заказ')
async def get_offer(message: Message, state: FSMContext):
    await message.answer('Введите id желаемого товара')
    await state.set_state(Offer.id)


@router.message(Offer.id)
async def hello(message: Message, state: FSMContext):
    try:
        prod_id = message.text
        await state.update_data(id=prod_id)
        data = requests.get(f'{main_api_url}/api/product/get/{prod_id}').json()
        print(data)
        name = data.get('title')
        desc = data.get('description')
        price = data.get('price')
        await message.answer(f'Название товара: {name}\nОписание: {desc}\nЦена: {price}\n\nОформить заказ?',
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
        data = await state.get_data()
        prod_id = data.get('id')
        address = message.text
        await state.update_data(address=address)
        buyer_id = message.from_user.id
        user_id = requests.get(f'{main_api_url}/api/product/get/{prod_id}').json().get('user')
        data = {'product': prod_id, 'address': address, 'buyer_id': buyer_id, 'user': user_id}
        offer_id = requests.post(f'{main_api_url}/api/orders/create/', data=data).json()
        print(offer_id)
        await message.answer(f'Ваш заказ успешно зарегистрирован. ID товара: {prod_id}, '
                                          f'адрес доставки: {address}, номер заказа: {offer_id}.', reply_markup=make_offer_kb)
