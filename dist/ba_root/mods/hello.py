import bascenev1 as bs

#don't define activity variable at top to reduce redundancy; few cmds like 'end' wont work since Activity won't die

def get_entity(client_id):
    ros = bs.get_game_roster()
    for entity in ros:
        if entity["client_id"] == client_id:
            return entity
    return None

def hello():
    activity = bs.get_foreground_host_activity()
    print(bs.get_public_party_max_size())
    bs.broadcastmessage(f"konnichiwa chibi!", clients=None, transient=True, color=(0, 0.5, 1))
    return None

def end(client_id):
    print("end is called")
    try:
        game = bs.get_foreground_host_activity()
        with game.context:
            game.end_game()
        entity = get_entity(client_id)
        if entity:
            name = entity["players"][0]["name"]
            bs.broadcastmessage(f"{name} ended game", clients=None, transient=True, color=(0, 0.5, 1))
    except Exception as e:
        print(e)
    return None

def kick(msg, client_id):
    print("called kick")
    args = msg.split()
    rat = int(args[1])
    reason = " ".join(args[2:])

    try:
        bs.disconnect_client(rat, ban_time=60*5)  # seconds
        rat_entity = get_entity(rat)
        admin_entity = get_entity(client_id)
        if rat_entity and admin_entity:
            nameRat = rat_entity["display_string"]
            name = admin_entity["players"][0]["name"]
            bs.broadcastmessage(f"{name} Kicked {nameRat}, reason: {reason}", transient=True, color=(0, 0.5, 1), clients=None)
            print(f"{name} Kicked {nameRat}, reason: {reason}")
    except Exception as e:
        print(e)
    return None

def tint(msg):
    args = msg.split()
    r, g, b = float(args[1]), float(args[2]), float(args[3])
    try:
        # print(dir(activity.globalsnode))
        activity = bs.get_foreground_host_activity()
        activity.globalsnode.tint = (r, g, b)
    except Exception as e:
        print(e)
    return None

def nv():
    def is_close(a, b, tol=1e-5):
        return all(abs(x - y) < tol for x, y in zip(a, b))

    try:
        activity = bs.get_foreground_host_activity()
        nv_tint = (0.4, 0.4, 1.0)
        nv_ambient = (1.5, 1.5, 1.5)
        
        if is_close(activity.globalsnode.tint, nv_tint):
            activity.globalsnode.tint = (1, 1, 1)
            activity.globalsnode.ambient_color = (1, 1, 1)
            #print(activity.globalsnode.tint)
            bs.broadcastmessage("Night Mode off", transient=True, color=(0, 0.5, 1), clients=None)
        else:
            activity.globalsnode.tint = nv_tint
            activity.globalsnode.ambient_color = nv_ambient
            #print(activity.globalsnode.tint)
            bs.broadcastmessage("Night Mode on", transient=True, color=(0, 0.5, 1), clients=None)
    except Exception as e:
        print(e)
    return None


def pause(client_id):
    activity = bs.get_foreground_host_activity()
    if activity.globalsnode.paused:
        return None
    try:
        activity.globalsnode.paused = True
        entity = get_entity(client_id)
        if entity:
            name = entity["players"][0]["name"]
            bs.broadcastmessage(f"{name} paused the game", transient=True, color=(0, 0.5, 1), clients=None)
    except Exception as e:
        print(e)
    return None

def resume(client_id):
    activity = bs.get_foreground_host_activity()
    if not activity.globalsnode.paused:
        return None
    try:
        activity.globalsnode.paused = False
        entity = get_entity(client_id)
        if entity:
            name = entity["players"][0]["name"]
            bs.broadcastmessage(f"{name} resumed the game", transient=True, color=(0, 0.5, 1), clients=None)
    except Exception as e:
        print(e)
    return None

def slowmo():
    try:
        activity = bs.get_foreground_host_activity()
        print(activity.globalsnode.slow_motion)
        if activity.globalsnode.slow_motion == True:
            activity.globalsnode.slow_motion = False
            bs.broadcastmessage("Epic mode off", transient=True, color=(0, 0.5, 1), clients=None)
        else:
            activity.globalsnode.slow_motion = True
            bs.broadcastmessage("Epic mode on", transient=True, color=(0, 0.5, 1), clients=None)
    except Exception as e:
        print(e)
    return None

#bs.get_public_party_max_size
#bs.set_public_party_max_size
#bs.get_chat_messages
#bs.SessionData
#bs.Stats
#bs.get_game_roster
def maxplayers(msg):
    args = msg.split()
    size = int(args[1])
    if 1 < size < 100:
        try:
            bs.set_public_party_max_size(size)
            #print(bs.get_public_party_max_size())
            bs.broadcastmessage(f"Max players set to {size}", transient=True, color=(0, 0.5, 1), clients=None)
        except Exception as e:
            print(e)
    else:
        bs.broadcastmessage("Invalid size. Must be between 2 and 99.", transient=True, color=(1, 0, 0), clients=None)
    return None