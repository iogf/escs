"""
"""

from quickirc import Irc, Misc, send_cmd, send_msg
from untwisted.network import SuperSocket
from untwisted.client import Client, lose
from untwisted.sock_writer  import SockWriter
from untwisted.sock_reader import SockReader
from untwisted.event import CLOSE, CONNECT_ERR, CONNECT
from untwisted.splits import Terminator
from cspkg.core import Mode, Namespace, Plugin, Main
from cspkg.plugins.extra_mode import Extra
from os.path import basename
from cspkg.scan import Scan, Read
from cspkg.start import root
from cspkg.xstr import Xstr

H1 = '<%s> %s\n' 
H2 = 'Topic :%s\n' 
H3 = '>>> %s has left %s :%s<<<\n' 
H4 = '>>> %s has joined %s <<<\n' 
H5 = '>>> %s is now known as %s <<<\n'
H6 = 'Peers:%s\n'
H7 = '>>> Connection is down ! <<<\n'
H8 = '>>> %s has kicked %s from %s (%s) <<<\n'
H9 = '>>> %s sets mode %s %s on %s <<<\n'
H10 = '>>> Connection is down ! <<<\n'
H11 = '>>> %s [%s@%s] has quit :%s <<<\n' 

class EsircNS(Namespace):
    pass

class Esirc(Mode):
    pass

class ChannelController(Plugin):
    """
    """
    def __init__(self, xstr, irc, chan):
        super().__init__(xstr)
        self.irc   = irc
        self.xstr  = xstr
        self.chan  = chan
        self.peers = set()

        events = (('PRIVMSG->%s' % chan , self.e_privmsg), 
        ('332->%s' % chan, self.e_332), 
        ('PART->%s' % chan, self.e_part), 
        ('JOIN->%s' % chan, self.e_join), 
        # ('*NICK', self.e_nick),
        ('NICK', self.e_nick),
        ('QUIT', self.e_quit),
        ('353->%s' % chan, self.e_353), 
        ('KICK->%s' % chan, self.e_kick), 
        ('MODE->%s' % chan, self.e_mode),
        (CLOSE, self.e_close))

        def unset(con, *args):
            for event, handle in events:
                irc.con.del_map(event, handle)

        for key, value in events:
            irc.con.add_map(key, value)

        irc.con.once('*PART->%s' % chan, unset)
        irc.con.add_map('*KICK->%s' % chan, unset)

        self.add_kmap(EsircNS, Main, '<Destroy>', 
        lambda event: unset(irc.con), add=True)

        # When xstr is destroyed, it sends a PART.
        xstr.bind('<Destroy>', lambda event: 
        send_cmd(irc.con, 'PART %s' % chan), add=True)
    
        # Hook to send msgs.
        self.add_kmap(EsircNS, Esirc, '<Key-i>', lambda event: Read(
        events={'<Escape>': lambda wid: True, 
        '<Tab>' : self.c_nick, '<Return>': lambda wid: 
        self.send_cmsg(wid, chan)}))

        # It unbinds the above callback.
        # In case the part command was sent by text
        # by the user. After part it should destroy the
        # xstr.
        irc.con.once('*PART->%s' % chan, lambda con, *args: 
        xstr.unbind('<Destroy>'))

    def e_privmsg(self, con, nick, user, host, msg):
        self.xstr.append(H1 % (nick, msg), '(ESIRC-PRIVMSG)')

    def e_join(self, con, nick, user, host):
        self.peers.add(nick.lower())
        self.xstr.append(H4 % (nick, self.chan), '(ESIRC-JOIN)')

    def e_mode(self, con, nick, user, host, mode, target=''):
        self.xstr.append(H9 % (nick, self.chan, 
        mode, target), '(ESIRC-MODE)')

    def e_part(self, con, nick, user, host, msg):
        self.peers.remove(nick.lower())
        self.xstr.append(H3 % (nick, self.chan, msg), '(ESIRC-PART)')

    def e_kick(self, con, nick, user, host, target, msg):
        self.xstr.append(H8 % (nick, target, 
        self.chan, msg), '(ESIRC-KICK)')

    def e_nick(self, con, nicka, user, host, nickb):
        self.peers.remove(nicka.lower())
        self.xstr.append(H5 % (nicka, nickb), '(ESIRC-NICK)')
        self.peers.add(nickb.lower())

    def e_close(self, con, *args):
        self.xstr.append(H7, '(ESIRC-CLOSE)')

    def e_332(self, con, addr, nick, msg):
        self.xstr.append(H2 % msg, '(ESIRC-332)')

    def e_353(self, con, prefix, nick, mode, peers):
        self.peers.update(peers.lower().split(' '))
        self.xstr.append(H6 % peers, '(ESIRC-353)')

    def e_quit(self, con, nick, user, host, msg=''):
        if not nick.lower() in self.peers: return
        self.xstr.append(H11 % (nick, user, 
        host, msg), '(ESIRC-QUIT)')

    def c_nick(self, wid):
        data = wid.get()
        size = len(data)
        data = data.rsplit(' ', 1)[-1]

        for ind in self.peers:
            if ind.startswith(data):
                index = size - len(data)
                wid.delete(index, size)
                wid.insert(index, ind)
                break
            pass

    def send_cmsg(self, wid, target):
        """
        """

        data = wid.get()
        self.xstr.append(H1 % (self.irc.misc.nick, data))
        send_msg(self.irc.con, target, data)
        wid.delete(0, 'end')

class PMsgController(Plugin):
    def __init__(self, xstr, irc, nick):
        super().__init__(xstr)
        self.irc = irc
        self.add_kmap(EsircNS, Esirc, '<Key-i>', 
        lambda event: Read(events={'<Escape>': lambda wid: True, 
        '<Return>': lambda wid: self.send_umsg(wid, nick)}))

    def send_umsg(self, wid, target):
        """
        """

        data = wid.get()
        self.xstr.append(H1 % (self.irc.misc.nick, data))
        send_msg(self.irc.con, target, data)
        wid.delete(0, 'end')

class IrcCommon(Plugin):
    def __init__(self, xstr, irc):
        super().__init__(xstr)
        self.irc = irc
        self.chmode(Esirc)
        self.add_kmap(EsircNS, Extra, '<Key-i>', 
        lambda event: self.chmode(Esirc))

        self.add_kmap(EsircNS, Main, '<<Chmode-IRC>>', 
        lambda event: xstr.mark_set('insert', 'end'))

        self.add_kmap(EsircNS, Esirc, 
        '<Control-e>', self.send_cmd)

        self.add_kmap(EsircNS, Esirc, 
        '<Control-c>',  self.open_private_channel)

    def send_cmd(self, event):
        """
        Used to drop irc commands.
        """

        scan = Scan()
        send_cmd(self.irc.con, scan.data)

    def open_private_channel(self, event):
        scan = Scan()
        xstr = root.note.create(scan.data)
        IrcCommon(xstr, self)
        PMsgController(xstr, self.irc, scan.data)
        return xstr

class ServerController(Plugin):
    def __init__(self, xstr, irc):
        super().__init__(xstr)
        self.irc = irc

        irc.con.add_map('*JOIN', self.e_mejoin)
        irc.con.add_map('PMSG', self.e_pmsg)

        irc.con.add_map('376', lambda con, *args: 
        send_cmd(irc.con, self.irc.irccmd))

        irc.con.add_map('376', self.auto_join)

        irc.con.add_map('PING', lambda con, prefix, servaddr: 
        send_cmd(irc.con, 'PONG :%s' % servaddr))

        send_cmd(irc.con, 'NICK %s' % self.irc.nick)
        send_cmd(irc.con, 'USER %s' % self.irc.user) 

        self.add_kmap(EsircNS, Main, '<Destroy>', 
        lambda event: send_cmd(irc.con, 'QUIT :escs rules!'), add=True)

    def auto_join(self, con, *args):
        for ind in self.irc.channels:
            send_cmd(con, 'JOIN %s' % ind)

    def e_mejoin(self, con, chan):
        xstr = root.note.create(chan)
        IrcCommon(xstr, self.irc)
        ChannelController(xstr, self.irc, chan)
        return xstr

    def create_private_channel(self, nick):
        xstr = root.note.create(nick)
        IrcCommon(xstr, self.irc)
        PMsgController(xstr, self.irc, nick)
        return xstr

    def e_pmsg(self, con, nick, user, host, target, msg):
        """
        Private messages sent to the user are handled here.
        """

        # Attempt to retrieve the xstr which corresponds
        # to the target/user.
        files = iter(Xstr.get_opened_files(root).items())
        targets = dict(list(map(lambda ind: 
        (basename(ind[0].lower()), ind[1]), files)))

        try:
            xstr = targets[nick.lower()]
        except KeyError:
            xstr = self.create_private_channel(nick)
        xstr.append(H1 % (nick, msg))

class IrcMode:
    """
    Controls basic irc events and installs basic commands.
    """

    TAGCONF = {
    '(ESIRC-PRIVMSG)': {'foreground': '#688B96'},
    '(ESIRC-JOIN)': {'foreground': '#F06EF0'},
    '(ESIRC-PART)': {'foreground': '#F0BDAD'},
    '(ESIRC-QUIT)': {'foreground': '#4EDB1F'},
    '(ESIRC-NICK)': {'foreground': '#E9F0AD'},
    '(ESIRC-KICK)': {'foreground': '#FC8D9A'},
    '(ESIRC-353)': {'foreground': '#BF9163'},
    '(ESIRC-332)': {'foreground': '#81BFFC'},
    '(ESIRC-CLOSE)': {'foreground': '#A7F2E9'}}
    
    def __init__(self, addr, port, user, nick, irccmd, channels=[], encoding='utf8'):
        con      = SuperSocket()
        self.con = con
        con.connect_ex((addr, int(port)))
        Client(con)

        con.add_map(CONNECT, self.on_connect)
        con.add_map(CONNECT_ERR, self.e_connect_err)
        self.misc     = None
        self.addr     = addr
        self.port     = port
        self.user     = user
        self.nick     = nick
        self.irccmd   = irccmd
        self.channels = channels
        self.encoding = encoding

    def on_connect(self, con):
        xstr = root.note.create(self.addr)

        SockWriter(con)
        SockReader(con)
        Terminator(con)
        Irc(con)
        self.misc = Misc(con)
        IrcCommon(xstr, self)
        ServerController(xstr, self)

        con.add_map(CLOSE, lambda con, err: lose(con))

        con.add_map(Terminator.FOUND, 
        lambda con, data: xstr.append('%s\n' % data.decode(self.encoding)))

    def e_connect_err(self, con, err):
        print('not connected')

