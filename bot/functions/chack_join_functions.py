# region imports


from typing import Optional

# endregion

async def check_join(user_id: int, send_message: Optional[bool] = False, invited_by_user: int | None = None) -> bool:
    "return : yek list az button ha baraya channel haye delete shode ast"

    with Session(engine) as session:
        channels = session.query(Channel).all()

        if not channels:
            return True

        not_joined = []
        not_admin = []

        for channel in channels:

            try:

                await client(GetParticipantRequest(PeerChannel(channel.channel_id), PeerUser(int(user_id))))

            except UserNotParticipantError:
                not_joined.append(channel)
            
            except (ChatAdminRequiredError, ChannelPrivateError):
                not_admin.append(channel)
                session.delete(channel)

            except Exception as e:
                print(e)
                return True
        
        session.commit()

        for channel in not_admin:
            try:
                await client.send_message((BotConfig.CREATOR_USER_ID), message=Strings.channel_deleted(channel))
            except Exception as e:
                print(e)
        
        if not not_joined:
            return True

        try:
            if send_message and not_joined:
                await client.send_message(PeerUser(user_id), Strings.JOIN_TO_CHANNELS, buttons=UrlButtons.channels_locked(not_joined, invited_user_id=invited_by_user))
        except Exception as e:
            print("error in send message for join channel : ". e)
        finally:
            return False

