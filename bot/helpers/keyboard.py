#!/usr/bin/env python3
# This is bot coded by Abhijith N T and used for educational purposes only
# https://github.com/abhint
# Copyright ABHIJITH N T
# Thank you https://github.com/pyrogram/pyrogram

from pyrogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton
)


def server_select(file_size: int):
    upload_selection = [
        [
            InlineKeyboardButton(
                "cloudkp.com",
                callback_data=f"cloudkp"
            )
        ],
        [
            InlineKeyboardButton(
                "gofile.io",
                callback_data=f"gofileio"
            )
        ],
        [
            InlineKeyboardButton(
                "filemoon",
                callback_data=f"filemoon"
            )
    ]
    ]
    if file_size < 1e+8:
        # 1e+8 is 100000000.0
        upload_selection.append([
            InlineKeyboardButton(
                "File.io",
                callback_data=f"fileio"
            )
        ])
    return InlineKeyboardMarkup(upload_selection)
