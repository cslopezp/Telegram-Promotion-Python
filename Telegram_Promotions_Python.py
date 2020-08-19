import csv
import random
import sys
import time
import traceback

from telethon.errors.rpcerrorlist import PeerFloodError, UserPrivacyRestrictedError, UserIdInvalidError, \
    ChannelPrivateError, ChatWriteForbiddenError, UserNotMutualContactError, ChannelInvalidError, UserKickedError
from telethon.sync import TelegramClient
from telethon.tl import functions
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel, InputPeerUser, PeerChannel, ChannelParticipantsAdmins, \
    ChannelParticipantCreator, ChannelParticipantsSearch
from datetime import date, timedelta, datetime

input_file_conn = 'connections.csv'

cfg_file_conn = 'configmembersadding.txt'

print ("       ")
print ("*** ------------------------------------------------------------------------------ ***")
print ("*** --- IMPORTANT NOTE --- ***")
print ("Please make sure the connections are within the group/channel to be scrapped")
print ("Please make sure the connections are within the target group/channel to add members...")
print ("       ... and to have the largest number of members added it is better that the...")
print ("       ... connections are within the origin group ")
print ("*** ------------------------------------------------------------------------------ ***")
print ("       ")
print ("reading connections.csv...      ")
print ("       ")

# changing profile --> connections
v_connections = [ ]
s0 = 1
s1 = 0
s2 = 0
s3 = 0
s4 = 0
s5 = 0
s6 = 0
s7 = 0
s8 = 0
s9 = 0
s10 = 0
s11 = 0
s12 = 0
s13 = 0
s14 = 0
s15 = 0
s16 = 0
s17 = 0

with open (cfg_file_conn, encoding = 'UTF-8') as f:
    row_cfg = csv.reader (f, delimiter = ",", lineterminator = "\n")
    next (row_cfg, None)
    for row in row_cfg:
        v_conn = {}
        mode = int (row[ 0 ])
        v_blocks = int (row[ 1 ])
        v_seconds_block = int (row[ 2 ])
        v_seconds_start = int (row[ 3 ])
        v_seconds_end = int (row[ 4 ])

with open (input_file_conn, encoding = 'UTF-8') as f:
    rows = csv.reader (f, delimiter = ",", lineterminator = "\n")
    next (rows, None)
    v_cont = 0
    for row in rows:
        v_conn = {}
        v_conn[ 'api_index' ] = v_cont
        v_conn[ 'api_id' ] = row[ 0 ]
        v_conn[ 'api_hash' ] = (row[ 1 ])
        v_conn[ 'phone' ] = row[ 2 ]
        v_connections.append (v_conn)
        v_cont = v_cont + 1

print ('API''s ')
a = 0
print ('          [API_ID]      [API_HASH]                         [PHONE]')
for d in v_connections:
    print ('      ' + str (a) + '-  ' + d[ 'api_id' ] + '       ' + d[ 'api_hash' ] + '   ' + d[ 'phone' ])
    a += 1

# print ('      ' + str (a) + '-  Do Nothing and exit')

# print(v_connections.stringify())
# print('  datos  '.join(map(str, v_connections)) )

# v_conn_index = input ("Choose an API to work with: ")
v_conn_index = 0

if int (v_conn_index) < int (a):

    target_conn = v_connections[ int (v_conn_index) ]

    api_id = target_conn[ 'api_id' ]
    api_hash = target_conn[ 'api_hash' ]
    phone = target_conn[ 'phone' ]
    clients0 = TelegramClient (phone, api_id, api_hash)
    clients0.connect ()

    if not clients0.is_user_authorized ():
        clients0.send_code_request (phone)
        clients0.sign_in (phone, input ('Enter the code sent to your Telegram: '))
    s = 0
    v_option = '0';

    while v_option != '5':
        print ('Choose a option:')
        print ('      ' + '1. Scrape Members')
        print ('      ' + '2. Adding Members')
        print ('      ' + '3. Remove common Members')
        print ('      ' + '4. Messages to Members')
        print ('      ' + '5. Exit')
        v_option = input ('Enter a Number: ')
        # ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if v_option == '1':
            # if (s0 == 1 or s1 == 1 or s2 == 1 or s3 == 1):
            #    if (v_conn_index == 0):
            #        clients0.disconnect ()
            #    if (v_conn_index == 1):
            #        clients1.disconnect ()
            #    if (v_conn_index == 2):
            #        clients2.disconnect ()
            #    if (v_conn_index == 3):
            #        clients3.disconnect ()
            # client.reconnect ()

            chats = [ ]
            last_date = None
            chunk_size = 200
            groups = [ ]
            result = clients0 (
                GetDialogsRequest (offset_date = last_date, offset_id = 0, offset_peer = InputPeerEmpty (),
                                   limit = chunk_size, hash = 0))

            chats.extend (result.chats)
            for chat in chats:
                try:
                    if (chat.megagroup == True or chat.broadcast == True):
                        groups.append (chat)
                except:
                    continue
                # print('  datos  '.join(map(str, chats)) )

            print ('   Choose a group to scrape members from:')
            i = 0
            for g in groups:
                print ('      ' + str (i) + '- ' + g.title)
                i += 1
            print ('     ' + str (i) + '-  Do Nothing and exit')
            g_index = input ("           Enter a Number: ")

            if int (g_index) < i:
                target_group = groups[ int (g_index) ]
           #     invitation = clients0 (functions.messages.ExportChatInviteRequest ( target_group.id))
               # print (invitation.stringify())
                #event  = clients0.get_admin_log(entity = target_group.id , limit = 15 , invite=True)
               # print ( ' hola '.join(map(str, event)) )


                g_days = input ("           At least How many days active to fetch members?: ")
                v_fecha = date.today () - timedelta (days = int (g_days))
                print ('Fetching active Members... after ', v_fecha.isoformat ())
                #print(' datos de grupo' + target_group.stringify())
                try:
                    all_participants = [ ]
                    all_admins = [ ]
                    all_participants = clients0.get_participants (target_group, aggressive = True)
                    all_admins = clients0.get_participants (target_group, aggressive = True,
                                                            filter = ChannelParticipantsAdmins)
                    # all_creator = client0.get_participants(target_group, filter=ChannelParticipantCreator)
                    v_namefile = input ("specify file  name (*.txt / *.csv).... --> ")
                    print ('Saving In file...')
                    z = 0
                    with open (v_namefile, "w", encoding = 'UTF-8') as f:
                        writer = csv.writer (f, delimiter = ",", lineterminator = "\n")
                        writer.writerow ([ 'username', 'user id', 'access hash', 'name', 'group', 'group id' ])
                        # print ('  ***  '.join (map (str, all_participants)))
                        for user in all_participants:
                            v_admin = 0
                            for i, dato in enumerate (all_admins):
                                if user.id == dato.id:
                                    v_admin = 1
                                    # print (' creador ' + str(user.id))
                            # print(user.stringify())
                            # usuario = clients0.get_entity (target_group.id)
                            #print (user.stringify ())
                            try:
                                if  v_admin == 0 and datetime.date (user.status.was_online) >= v_fecha:
                                    if user.username:
                                        username = user.username
                                    else:
                                        username = ""
                                    if user.first_name:
                                        first_name = user.first_name
                                    #  print(user.status.was_online)
                                    else:
                                        first_name = ""
                                    if user.last_name:
                                        last_name = user.last_name
                                    else:
                                        last_name = ""
                                    name = (first_name + ' ' + last_name).strip ()
                                    writer.writerow (
                                        [ username, user.id, user.access_hash, name, target_group.title,
                                          target_group.id ])
                            except:
                                if not (hasattr (user, 'was_online')):
                                    z = z + 1
                    print ('Members skipped because have private settings...' + str (z))
                    print ('Members scraped successfully.')
                except:
                    traceback.print_exc ()
                    print ("*** --- Is not a supergroup or channel or invalid permissions ***")
        # --------------------------------------------------------------------------------------------------------------------------------------------------------------------------
        if v_option == '2':  # ADDING MEMBERS

            v_i = 1
            # while v_i <= v_cant_conn:
            # client[]
            v_error = 0
            a = 0

            print ('          [API_ID]      [API_HASH]                         [PHONE]')
            for d in v_connections:
                print (
                    '      ' + str (d[ 'api_index' ]) + '-  ' + d[ 'api_id' ] + '       ' + d[ 'api_hash' ] + '   ' + d[
                        'phone' ])
                a += 1
                api_id = d[ 'api_id' ]
                api_hash = d[ 'api_hash' ]
                phone = d[ 'phone' ]
                if d[ 'api_index' ] == 0:
                    if s0 == 0:
                        clients0 = TelegramClient (phone, api_id, api_hash)
                    if not clients0.is_connected ():
                        print ('          Client connectimg...')
                        clients0.connect ()
                        s0 = 1

                    try:
                        if not clients0.is_user_authorized ():
                            clients0.send_code_request (phone)
                            clients0.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients0.is_connected ():
                            myself = clients0.get_me ()
                            print ('          Client connection authorized...')
                            s0 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 1:
                    if s1 == 0:
                        clients1 = TelegramClient (phone, api_id, api_hash)
                    if not clients1.is_connected ():
                        print ('          Client connectimg...')
                        clients1.connect ()
                        s1 = 1
                    try:
                        if not clients1.is_user_authorized ():
                            clients1.send_code_request (phone)
                            clients1.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients1.is_connected ():
                            myself1 = clients1.get_me ()
                            print ('          Client connection authorized...')
                            result1 = clients1 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s1 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 2:
                    if s2 == 0:
                        clients2 = TelegramClient (phone, api_id, api_hash)
                    if not clients2.is_connected ():
                        print ('          Client connectimg...')
                        clients2.connect ()
                        s2 = 1
                    try:
                        if not clients2.is_user_authorized ():
                            clients2.send_code_request (phone)
                            clients2.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients2.is_connected ():
                            myself2 = clients2.get_me ()
                            print ('          Client connection authorized...')
                            result2 = clients2 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s2 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 3:
                    if s3 == 0:
                        clients3 = TelegramClient (phone, api_id, api_hash)
                    if not clients3.is_connected ():
                        print ('          Client connectimg...')
                        clients3.connect ()
                        s3 = 1
                    try:
                        if not clients3.is_user_authorized ():
                            clients3.send_code_request (phone)
                            clients3.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients3.is_connected ():
                            myself3 = clients3.get_me ()
                            print ('          Client connection authorized...')
                            result3 = clients3 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s3 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 4:
                    if s4 == 0:
                        clients4 = TelegramClient (phone, api_id, api_hash)
                    if not clients4.is_connected ():
                        print ('          Client connectimg...')
                        clients4.connect ()
                        s4 = 1
                    try:
                        if not clients4.is_user_authorized ():
                            clients4.send_code_request (phone)
                            clients4.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients4.is_connected ():
                            myself4 = clients4.get_me ()
                            print ('          Client connection authorized...')
                            result4 = clients4 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s4 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 5:
                    if s5 == 0:
                        clients5 = TelegramClient (phone, api_id, api_hash)
                    if not clients5.is_connected ():
                        print ('          Client connectimg...')
                        clients5.connect ()
                        s5 = 1
                    try:
                        if not clients5.is_user_authorized ():
                            clients5.send_code_request (phone)
                            clients5.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients5.is_connected ():
                            myself5 = clients5.get_me ()
                            print ('          Client connection authorized...')
                            result5 = clients5 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s5 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 6:
                    if s6 == 0:
                        clients6 = TelegramClient (phone, api_id, api_hash)
                    if not clients6.is_connected ():
                        print ('          Client connectimg...')
                        clients6.connect ()
                        s6 = 1
                    try:
                        if not clients6.is_user_authorized ():
                            clients6.send_code_request (phone)
                            clients6.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients6.is_connected ():
                            myself6 = clients6.get_me ()
                            print ('          Client connection authorized...')
                            result6 = clients6 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s6 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 7:
                    if s7 == 0:
                        clients7 = TelegramClient (phone, api_id, api_hash)
                    if not clients7.is_connected ():
                        print ('          Client connectimg...')
                        clients7.connect ()
                        s7 = 1
                    try:
                        if not clients7.is_user_authorized ():
                            clients7.send_code_request (phone)
                            clients7.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients7.is_connected ():
                            myself1 = clients7.get_me ()
                            print ('          Client connection authorized...')
                            result7 = clients7 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s7 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 8:
                    if s8 == 0:
                        clients8 = TelegramClient (phone, api_id, api_hash)
                    if not clients8.is_connected ():
                        print ('          Client connectimg...')
                        clients8.connect ()
                        s8 = 1
                    try:
                        if not clients8.is_user_authorized ():
                            clients8.send_code_request (phone)
                            clients8.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients8.is_connected ():
                            myself8 = clients8.get_me ()
                            print ('          Client connection authorized...')
                            result8 = clients8 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s8 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 9:
                    if s9 == 0:
                        clients9 = TelegramClient (phone, api_id, api_hash)
                    if not clients9.is_connected ():
                        print ('          Client connectimg...')
                        clients9.connect ()
                        s9 = 1
                    try:
                        if not clients9.is_user_authorized ():
                            clients9.send_code_request (phone)
                            clients9.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients9.is_connected ():
                            myself9 = clients9.get_me ()
                            print ('          Client connection authorized...')
                            result9 = clients9 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s9 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 10:
                    if s10 == 0:
                        clients10 = TelegramClient (phone, api_id, api_hash)
                    if not clients10.is_connected ():
                        print ('          Client connectimg...')
                        clients10.connect ()
                        s10 = 1
                    try:
                        if not clients10.is_user_authorized ():
                            clients10.send_code_request (phone)
                            clients10.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients10.is_connected ():
                            myself10 = clients10.get_me ()
                            print ('          Client connection authorized...')
                            result10 = clients10 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s10 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 11:
                    if s11 == 0:
                        clients11 = TelegramClient (phone, api_id, api_hash)
                    if not clients11.is_connected ():
                        print ('          Client connectimg...')
                        clients11.connect ()
                        s11 = 1
                    try:
                        if not clients11.is_user_authorized ():
                            clients11.send_code_request (phone)
                            clients11.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients11.is_connected ():
                            myself11 = clients11.get_me ()
                            print ('          Client connection authorized...')
                            result11 = clients11 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s11 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 12:
                    if s12 == 0:
                        clients12 = TelegramClient (phone, api_id, api_hash)
                    if not clients12.is_connected ():
                        print ('          Client connectimg...')
                        clients12.connect ()
                        s12 = 1
                    try:
                        if not clients12.is_user_authorized ():
                            clients12.send_code_request (phone)
                            clients12.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients12.is_connected ():
                            myself12 = clients12.get_me ()
                            print ('          Client connection authorized...')
                            result12 = clients12 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s12 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 13:
                    if s13 == 0:
                        clients13 = TelegramClient (phone, api_id, api_hash)
                    if not clients13.is_connected ():
                        print ('          Client connectimg...')
                        clients13.connect ()
                        s13 = 1
                    try:
                        if not clients13.is_user_authorized ():
                            clients13.send_code_request (phone)
                            clients13.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients13.is_connected ():
                            myself13 = clients13.get_me ()
                            print ('          Client connection authorized...')
                            result13 = clients13 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s13 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 14:
                    if s14 == 0:
                        clients14 = TelegramClient (phone, api_id, api_hash)
                    if not clients14.is_connected ():
                        print ('          Client connectimg...')
                        clients14.connect ()
                        s14 = 1
                    try:
                        if not clients14.is_user_authorized ():
                            clients14.send_code_request (phone)
                            clients14.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients14.is_connected ():
                            myself14 = clients14.get_me ()
                            print ('          Client connection authorized...')
                            result14 = clients14 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s14 = 14
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 15:
                    if s15 == 0:
                        clients15 = TelegramClient (phone, api_id, api_hash)
                    if not clients15.is_connected ():
                        print ('          Client connectimg...')
                        clients15.connect ()
                        s15 = 1
                    try:
                        if not clients15.is_user_authorized ():
                            clients15.send_code_request (phone)
                            clients15.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients15.is_connected ():
                            myself15 = clients15.get_me ()
                            print ('          Client connection authorized...')
                            result15 = clients15 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s15 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 16:
                    if s16 == 0:
                        clients16 = TelegramClient (phone, api_id, api_hash)
                    if not clients16.is_connected ():
                        print ('          Client connectimg...')
                        clients16.connect ()
                        s16 = 1
                    try:
                        if not clients16.is_user_authorized ():
                            clients16.send_code_request (phone)
                            clients16.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients16.is_connected ():
                            myself16 = clients16.get_me ()
                            print ('          Client connection authorized...')
                            result16 = clients16 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s16 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break
                if d[ 'api_index' ] == 17:
                    if s17 == 0:
                        clients17 = TelegramClient (phone, api_id, api_hash)
                    if not clients17.is_connected ():
                        print ('          Client connectimg...')
                        clients17.connect ()
                        s17 = 1
                    try:
                        if not clients17.is_user_authorized ():
                            clients17.send_code_request (phone)
                            clients17.sign_in (phone, input ('Enter the code sent to your Telegram: '))
                        if clients17.is_connected ():
                            myself17 = clients17.get_me ()
                            print ('          Client connection authorized...')
                            result17 = clients17 (
                                GetDialogsRequest (offset_date = None, offset_id = 0, offset_peer = InputPeerEmpty (),
                                                   limit = 200, hash = 0))
                            s17 = 1
                    except:
                        v_error = 1
                        traceback.print_exc ()
                        print (' ')
                        break

            print (' Clients connections checked...')
            if v_error == 0:
                input_file = input ('Enter source file name:  ')
                users = [ ]
                try:
                    with open (input_file, encoding = 'UTF-8') as f:
                        rows = csv.reader (f, delimiter = ",", lineterminator = "\n")
                        next (rows, None)
                        for row in rows:
                            user = {}
                            user[ 'username' ] = row[ 0 ]
                            user[ 'id' ] = int (row[ 1 ])
                            user[ 'access_hash' ] = int (row[ 2 ])
                            user[ 'name' ] = row[ 3 ]
                            user[ 'group' ] = row[ 4 ]
                            user[ 'group_id' ] = int (row[ 5 ])
                            users.append (user)

                    chats = [ ]
                    last_date = None
                    chunk_size = 200
                    groups = [ ]

                    result = clients0 (GetDialogsRequest (
                        offset_date = last_date,
                        offset_id = 0,
                        offset_peer = InputPeerEmpty (),
                        limit = chunk_size,
                        hash = 0
                    ))
                    chats.extend (result.chats)

                    for chat in chats:
                        try:
                            if (chat.megagroup == True or chat.broadcast == True):
                                groups.append (chat)
                        except:
                            continue
                    print ('Choose a group to add members:')
                    i = 0
                    for group in groups:
                        print ('   [' + str (i) + '] - ' + group.title)
                        i += 1

                    g_index = input ("Enter a Number: ")
                    target_group = groups[ int (g_index) ]

                    n = 0
                    v_cont_conn = 0
                    print ("       ")
                    print ("*** ------------------------------- ***")
                    print ("*** --- CONFIGMEMBERSADDING.TXT --- ***")
                    print ("Amount of members (block) to change connection : " + str (v_blocks))
                    print ("After each block of members added, Total seconds of waiting  to change connection: " + str (
                        v_seconds_block))
                    print (str (v_seconds_start) + "..." + str (
                        v_seconds_end) + " seconds of waiting after each member added.")
                    print ("*** ------------------------------- ***")
                    print ("       ")
                    v_linea = 1
                    for user in users:
                        n += 1
                        v_linea += 1
                        if n % v_blocks == 0:
                            time.sleep (v_seconds_block)
                            v_cont_conn = v_cont_conn + 1
                            if v_cont_conn > a - 1:
                                v_cont_conn = 0
                            # Change connections

                        try:
                            print ('Using connection --> [' + str (v_cont_conn) + ']')
                            print ('Line ' + str (v_linea) + "  Adding {}".format (user[ 'id' ]))
                            if mode == 1:
                                if user[ 'username' ] == "":
                                    continue
                                user_to_add = clients0.get_input_entity (user[ 'username' ])
                                # print (' MODE 1    usuario  ' + user_to_add.stringify ())
                            elif mode == 2:
                                user_to_add = InputPeerUser (user[ 'id' ], user[ 'access_hash' ])
                                # print (' MODE 2    usuario  ' + user_to_add.stringify ())
                            else:
                                sys.exit ("Invalid Mode Selected. Please Try Again.")
                            if v_cont_conn == 0:
                                hash0 = clients0.get_input_entity (PeerChannel (target_group.id))
                                target_group_entity = InputPeerChannel (target_group.id, hash0.access_hash)
                                try:
                                    clients0 (InviteToChannelRequest (target_group_entity, [ user_to_add ]))
                                except UserIdInvalidError:
                                    if user[ 'username' ] == "":
                                        continue
                                    print ('       searching second time...  ')
                                    user_to_add = clients0.get_input_entity (user[ 'username' ])
                                    clients0 (InviteToChannelRequest (target_group_entity, [ user_to_add ]))
                                    # print (' ERROR usuario  ' + user_to_add.stringify ())
                            if v_cont_conn == 1:
                                hash1 = clients1.get_input_entity (PeerChannel (target_group.id))
                                target_group_entity = InputPeerChannel (target_group.id, hash1.access_hash)
                                try:
                                    clients1 (InviteToChannelRequest (target_group_entity, [ user_to_add ]))
                                except UserIdInvalidError:
                                    if user[ 'username' ] == "":
                                        continue
                                    print ('       searching second time...  ')
                                    user_to_add = clients1.get_input_entity (user[ 'username' ])
                                    clients1 (InviteToChannelRequest (target_group_entity, [ user_to_add ]))
                                    # print (' ERROR usuario  ' + user_to_add.stringify ())
                            if v_cont_conn == 2:
                                hash2 = clients2.get_input_entity (PeerChannel (target_group.id))
                                target_group_entity = InputPeerChannel (target_group.id, hash2.access_hash)
                                try:
                                    clients2 (InviteToChannelRequest (target_group_entity, [ user_to_add ]))
                                except UserIdInvalidError:
                                    if user[ 'username' ] == "":
                                        continue
                                    print ('       searching second time...  ')
                                    user_to_add = clients2.get_input_entity (user[ 'username' ])
                                    clients2 (InviteToChannelRequest (target_group_entity, [ user_to_add ]))
                                    # print (' ERROR usuario  ' + user_to_add.stringify ())

                            if v_cont_conn == 3:
                                hash3 = clients3.get_input_entity (PeerChannel (target_group.id))
                                target_group_entity = InputPeerChannel (target_group.id, hash3.access_hash)
                                try:
                                    clients3 (InviteToChannelRequest (target_group_entity, [ user_to_add ]))
                                except UserIdInvalidError:
                                    if user[ 'username' ] == "":
                                        continue
                                    print ('       searching second time...  ')
                                    user_to_add = clients3.get_input_entity (user[ 'username' ])
                                    clients3 (InviteToChannelRequest (target_group_entity, [ user_to_add ]))
                                    # print (' ERROR usuario  ' + user_to_add.stringify ())

                            if v_cont_conn == 4:
                                hash4 = clients4.get_input_entity (PeerChannel (target_group.id))
                                target_group_entity = InputPeerChannel (target_group.id, hash4.access_hash)
                                try:
                                    clients4 (InviteToChannelRequest (target_group_entity, [ user_to_add ]))
                                except UserIdInvalidError:
                                    if user[ 'username' ] == "":
                                        continue
                                    print ('       searching second time...  ')
                                    user_to_add = clients4.get_input_entity (user[ 'username' ])
                                    clients4 (InviteToChannelRequest (target_group_entity, [ user_to_add ]))
                                    # print (' ERROR usuario  ' + user_to_add.stringify ())


                            print ('       Waiting for ' + str (v_seconds_start) + ' - ' + str (
                                v_seconds_end) + ' seconds..')
                            time.sleep (random.randrange (v_seconds_start, v_seconds_end))
                        except PeerFloodError:
                            n = v_blocks - 1
                            print ("       Connection[" + str (
                                v_cont_conn) + "]  Getting Flood Error FROM TELEGRAM.  Please TRY AGAIN AFTER SOME TIME WITH THIS CONNECTION.  Skipping.")
                            time.sleep (random.randrange (v_seconds_start, v_seconds_end))
                        except UserPrivacyRestrictedError:
                            print ("       The user's privacy settings do not allow you to do this. Skipping.")
                            time.sleep (random.randrange (v_seconds_start, v_seconds_end))
                        except ChannelPrivateError:
                            print ("       Connection[" + str (
                                v_cont_conn) + "]   CPE The channel specified is private and you lack permission to access it. or account connection is not in the group/channel,  Skipping.")
                            time.sleep (random.randrange (v_seconds_start, v_seconds_end))
                        except ChatWriteForbiddenError:
                            print ("       Connection[" + str (
                                v_cont_conn) + "]   You can't write in this chat (caused by InviteToChannelRequest), check permissions")
                            time.sleep (random.randrange (v_seconds_start, v_seconds_end))
                        except UserNotMutualContactError:
                            print ("       Connection[" + str (
                                v_cont_conn) + "]  The provided user is not a mutual contact. Skipping")
                            time.sleep (random.randrange (v_seconds_start, v_seconds_end))
                        except UserIdInvalidError:
                            print (
                                '       searching second time... fail.  make sure connection account have access to source and target group/channel.  Or member settings changed. Skipping   ')
                            time.sleep (random.randrange (v_seconds_start, v_seconds_end))
                        except ValueError:
                            print ("       Connection[" + str (
                                v_cont_conn) + "]   ValueError for ...  make sure connection account have access to source and target group/channel.  Or member settings changed. Skipping   ")
                            time.sleep (random.randrange (v_seconds_start, v_seconds_end))
                        except ChannelInvalidError:
                            print ("       Connection[" + str (
                                v_cont_conn) + "]   CIE The channel specified is private and you lack permission to access it. or account connection is not in the group/channel,  Skipping.")
                            time.sleep (random.randrange (v_seconds_start, v_seconds_end))
                        except UserKickedError:
                            print ("       Connection[" + str (
                                v_cont_conn) + "]   This user was kicked from this supergroup/channel ,  Skipping.")
                            time.sleep (random.randrange (v_seconds_start, v_seconds_end))
                        except:
                            traceback.print_exc ()
                            print ("       Unexpected Error")
                            time.sleep (random.randrange (v_seconds_start, v_seconds_end))
                except FileNotFoundError:
                    print ("*** --- File not found ---  ***")
                except:
                    traceback.print_exc ()
                    print ("Unexpected Error")
        if v_option == '3':  # removing common members from source and targeted group
            source_users = [ ]
            target_users = [ ]
            print ("*** ------------------------------- ***")
            print ("*** --- Removing common members --- ***")
            try:
                source_file = input ('Enter the file name from which you want to remove common members (targeted group):  ')
                with open (source_file, encoding = 'UTF-8') as f:
                    rows = csv.reader (f, delimiter = ",", lineterminator = "\n")
                    next (rows, None)
                    for row in rows:
                        user = {}
                        user[ 'username' ] = row[ 0 ]
                        user[ 'id' ] = int (row[ 1 ])
                        user[ 'access_hash' ] = int (row[ 2 ])
                        user[ 'name' ] = row[ 3 ]
                        user[ 'group' ] = row[ 4 ]
                        user[ 'group_id' ] = int (row[ 5 ])
                        source_users.append (user)

                target_file = input ('Enter the file name with all members in my group:  ')
                with open (target_file, encoding = 'UTF-8') as f:
                    rows = csv.reader (f, delimiter = ",", lineterminator = "\n")
                    next (rows, None)
                    for row in rows:
                        user = {}
                        user[ 'username' ] = row[ 0 ]
                        user[ 'id' ] = int (row[ 1 ])
                        user[ 'access_hash' ] = int (row[ 2 ])
                        user[ 'name' ] = row[ 3 ]
                        user[ 'group' ] = row[ 4 ]
                        user[ 'group_id' ] = int (row[ 5 ])
                        target_users.append (user)

                v_finalfile = input ("Common members removed, specify new file name (*.txt / *.csv).... --> ")
                print ('Saving In new file...')
                with open (v_finalfile, "w", encoding = 'UTF-8') as f:
                    writer = csv.writer (f, delimiter = ",", lineterminator = "\n")
                    writer.writerow ([ 'username', 'user id', 'access hash', 'name', 'group', 'group id' ])
                    # print ('  ***  '.join (map (str, all_participants)))
                    encontrado = 0
                    for user in source_users:
                        encontrado = 0
                        for i in target_users:
                            if user[ 'id' ] == i[ 'id' ]:
                                encontrado = 1
                                break
                        if encontrado == 0:
                            writer.writerow ([user[ 'username' ], user[ 'id' ], user[ 'access_hash' ], user[ 'name' ],
                                                 user[ 'group' ], user[ 'group_id' ]])
                print ('Common Members removed and saved.')
            except FileNotFoundError:
                print ('*** --- File  not found ---  ***')
            except:
                traceback.print_exc ()

        if v_option == '4':  # messages to a group
            SLEEP_TIME = 8
            users = [ ]
            messages = ""
            v_message_file = 'message.txt'
            v_message_file = input ('Enter file name with message:  ')
            try:

                with open (v_message_file, encoding = 'UTF-8') as f:
                    rows = csv.reader (f, delimiter = "|", lineterminator = "\n")
                    #next (rows, None)
                    for row in rows:
                        try:
                            message = {}
                            #rint(' l  '  )
                            message[ 'message' ] = row[ 0 ]
                            messages = messages + row[0] + "\n"
                            #print(row[0])
                        except IndexError:
                            messages = messages + "\n"
                        #users.append (user)
                users_input_file = input ('Enter member''s file name to send a message:  ')
                with open (users_input_file, encoding = 'UTF-8') as f:
                    rows = csv.reader (f, delimiter = ",", lineterminator = "\n")
                    next (rows, None)
                    for row in rows:
                        user = {}
                        user[ 'username' ] = row[ 0 ]
                        user[ 'id' ] = int (row[ 1 ])
                        user[ 'access_hash' ] = int (row[ 2 ])
                        user[ 'name' ] = row[ 3 ]
                        users.append (user)

                #mode = int (input ("Enter 1 to send by user ID or 2 to send by username: "))
                mode = 2
                for user in users:
                    if mode == 2:
                        if user[ 'username' ] == "":
                            continue
                        receiver = clients0.get_input_entity (user[ 'username' ])
                    elif mode == 1:
                        receiver = InputPeerUser (user[ 'id' ], user[ 'access_hash' ])
                    else:
                        print ("Invalid Mode. Exiting.")
                        #client.disconnect (
                    message = random.choice (messages)
                    try:
                        print ("Sending Message to:", user[ 'name' ])
                        clients0.send_message (receiver, messages)
                        print ("Waiting {} seconds".format (SLEEP_TIME))
                        time.sleep (SLEEP_TIME)
                    except PeerFloodError:
                        print (
                            "Getting Flood Error from telegram. Script is stopping now. Please try again after some time.")
                    except UserPrivacyRestrictedError:
                        print ("       The user's privacy settings do not allow you to do this. Skipping.")
                    except ChannelPrivateError:
                        print ("       CPE The channel specified is private and you lack permission to access it. or account connection is not in the group/channel,  Skipping.")
                    except ChatWriteForbiddenError:
                        print ("       You can't write in this chat (caused by InviteToChannelRequest), check permissions")
                    except UserNotMutualContactError:
                        print ("       The provided user is not a mutual contact. Skipping")
                    except UserIdInvalidError:
                        print (
                            '       searching second time... fail.  make sure connection account have access to source and target group/channel.  Or member settings changed. Skipping   ')
                    except ValueError:
                        print ("       ValueError for ...  make sure connection account have access to source and target group/channel.  Or member settings changed. Skipping   ")
                    except ChannelInvalidError:
                        print ("       CIE The channel specified is private and you lack permission to access it. or account connection is not in the group/channel,  Skipping.")
                    except UserKickedError:
                        print ("       This user was kicked from this supergroup/channel ,  Skipping.")
                    #except Exception as e:
                    #    print ("Error:", e)
                    #    print ("Trying to continue...")
                    #    continue
                #client.disconnect ()
                print ("Done. Message sent to all users.")
            except FileNotFoundError:
                print ("File not Found")
            #except Exception as e:
            #    print (e)
    print ('bye bye')
