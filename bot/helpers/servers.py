from bot import LOGGER
from ..filetocloud import CloudBot
from .upload import server_upload
from ..helpers import download_media
from pyrogram.types import CallbackQuery
from hurry.filesize import size

logger = LOGGER(__name__)

link = ""


async def upload_handler(client: CloudBot, message: CallbackQuery, callback_data: str):
    global link
    if message.message.reply_to_message.video:
        file_name = message.message.reply_to_message.video.file_name
        file_ize = size(message.message.reply_to_message.video.file_size)
    elif message.message.reply_to_message.document:
        file_name = message.message.reply_to_message.document.file_name
        file_ize = size(message.message.reply_to_message.document.file_size)
    elif message.message.reply_to_message.audio:
        file_name = message.message.reply_to_message.audio.file_name
        file_ize = size(message.message.reply_to_message.audio.file_size)

    try:
        file_path = await download_media(client, message)
    except Exception as e:
        logger.error(f"{e}")
        await client.edit_message_text(
            chat_id=message.from_user.id,
            message_id=message.message.id,
            text=f"**File downloading error:** `{e}`",
        )
        return
    try:
        await client.edit_message_text(
            chat_id=message.message.chat.id,
            text="started uploading...",
            message_id=message.message.id
            # reply_markup=completedKeyboard(dl)
        )

        if callback_data.startswith('gofileio'):
            url = 'https://store1.gofile.io/uploadFile'
            response = await server_upload(file=file_path, url=url)
            link = await gofile_io(response)

        elif callback_data.startswith('fileio'):
            url = 'https://file.io/'
            response = await server_upload(file=file_path, url=url)
            link = await file_io(response)

        elif callback_data.startswith('anonymfiles'):
            url = 'https://api.anonfiles.com/upload'
            response = await server_upload(file=file_path, url=url)
            link = await anonfiles(response)
        await client.send_message(
            chat_id=message.message.chat.id,
            text=(f"File Name: `{file_name}`"
                  f"\nFile Size: `{file_ize}`"
                  f'\nURL: `{link}`'),
            reply_to_message_id=message.message.reply_to_message.id
    )
        await client.delete_messages(
            chat_id=message.message.chat.id,
            message_ids=message.message.id
        )
    except Exception as e:
        logger.error(f'{e}')
        await client.edit_message_text(
            chat_id=message.from_user.id,
            message_id=message.message.id,
            text=f"**File uploading error:** `{e}`",
        )
        return


async def anonfiles(response):
    return response['data']['file']['url']['short']


async def file_io(response):
    return response['link']


async def gofile_io(response):
    return response['data']['downloadPage']
