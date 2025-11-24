"""
"""

from quickirc import Irc, Misc, send_cmd, send_msg
from untwisted.network import SuperSocket
from untwisted.client import Client, lose
from untwisted.sock_writer  import SockWriter
from untwisted.sock_reader import SockReader
from untwisted.event import CLOSE, CONNECT_ERR, CONNECT
from untwisted.splits import Terminator
from cspkg.core import Namespace, Plugin, Main
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

class ChannelController(Plugin):
    """
    """
    def __init__(self, xstr, server, chan):
        super().__init__(xstr)
        self.server   = server
        self.xstr  = xstr
        self.chan  = chan
        self.peers = []

        events = (('PRIVMSG->%s' % self.chan , self.e_privmsg), 
        ('332->%s' % self.chan, self.e_332), 
        ('PART->%s' % self.chan, self.e_part), 
        ('JOIN->%s' % self.chan, self.e_join), 
        # ('*NICK', self.e_nick),
        ('353->%s' % self.chan, self.e_353), 
        ('KICK->%s' % self.chan, self.e_kick), 
        ('MODE->%s' % self.chan, self.e_mode),
        (CLOSE, self.e_close))

        def unset(con, *args):
            for event, handle in events:
                server.irc.con.del_map(event, handle)

        for event, handle in events:
            server.irc.con.add_map(event, handle)

        self.server.ccontrollers.append(self)
        self.server.irc.con.once('*PART->%s' % self.chan, 
        lambda *args: self.server.ccontrollers.remove(self))

        self.server.irc.con.add_map('*KICK->%s' % self.chan, 
        lambda *args: self.server.ccontrollers.remove(self))

        self.server.irc.con.once('*PART->%s' % self.chan, unset)
        self.server.irc.con.add_map('*KICK->%s' % self.chan, unset)

        # self.add_kmap(EsircNS, Main, '<Destroy>', 
        # lambda event: unset(irc.con), True)

        # When xstr is destroyed, it sends a PART.
        self.add_kmap(EsircNS, Main, '<Destroy>', lambda event: 
        send_cmd(self.server.irc.con, 'PART %s' % self.chan), True)
        self.chmode(Extra)

        self.add_kmap(EsircNS, Extra, '<Key-m>', lambda event: Read(
        events={'<Escape>': lambda wid: True, '<Return>': lambda wid: 
        self.send_cmsg(wid, self.chan)}, complete_words = self.peers), add=False)

    
        self.add_kmap(EsircNS, Extra, '<Key-e>', 
        self.server.send_cmd, add=False)

        self.add_kmap(EsircNS, Extra, '<Key-M>',  
        self.server.open_pchannel, add=False)

        self.xstr.tag_update(**self.server.irc.confs)

    def e_privmsg(self, con, nick, user, host, msg):
        self.xstr.append(H1 % (nick, msg), '(ESIRC-PRIVMSG)')

    def e_join(self, con, nick, user, host):
        self.peers.append(nick)
        self.xstr.append(H4 % (nick, self.chan), '(ESIRC-JOIN)')

    def e_mode(self, con, nick, user, host, mode, target=''):
        self.xstr.append(H9 % (nick, self.chan, 
        mode, target), '(ESIRC-MODE)')

    def e_part(self, con, nick, user, host, msg):
        if self.xstr.winfo_exists():
            self.xstr.append(H3 % (nick, 
                self.chan, msg), '(ESIRC-PART)')
        self.peers.remove(nick)

    def e_kick(self, con, nick, user, host, target, msg):
        self.xstr.append(H8 % (nick, target, 
        self.chan, msg), '(ESIRC-KICK)')

    def e_close(self, con, *args):
        self.xstr.append(H7, '(ESIRC-CLOSE)')

    def e_332(self, con, addr, nick, msg):
        self.xstr.append(H2 % msg, '(ESIRC-332)')

    def e_353(self, con, prefix, nick, mode, peers):
        self.peers.extend(peers.split(' '))
        self.xstr.append(H6 % peers, '(ESIRC-353)')

    def update_quit(self, nick, user, host, msg):
        self.peers.remove(nick)
        self.xstr.append(H11 % (nick, user, 
        host, msg), '(ESIRC-QUIT)')

    def update_nick(self, nicka, nickb):
        self.peers.remove(nicka)
        self.xstr.append(H5 % (nicka, nickb), '(ESIRC-NICK)')
        self.peers.append(nickb)

    def send_cmsg(self, wid, target):
        """
        """

        data = wid.get()
        self.xstr.append(H1 % (self.server.irc.misc.nick, data))
        send_msg(self.server.irc.con, target, data)
        wid.delete(0, 'end')

class PMsgController(Plugin):
    def __init__(self, xstr, server, nick):
        super().__init__(xstr)
        self.server = server
        self.nick = nick
        self.chmode(Extra)
        self.add_kmap(EsircNS, Extra, '<Key-m>', 
        lambda event: Read(events={'<Escape>': lambda wid: True, 
        '<Return>': lambda wid: self.send_umsg(wid, nick)}), add=False)

        # Register itself in the pcontrollers in lower case
        # in order to avoid opening other pchannel when user
        # changes nick to upper case. 

        # Its self.nick attribute should remain 
        # identical to the peer's nick for later usage.
        nick = nick.lower()
        self.server.pcontrollers[nick] = self
        self.add_kmap(EsircNS, Main, '<Destroy>',  lambda event: 
        self.server.pcontrollers.pop(nick), add=False)

        self.add_kmap(EsircNS, Extra, '<Key-e>', 
        self.server.send_cmd, add=False)

        self.add_kmap(EsircNS, Extra, '<Key-M>',  
        self.server.open_pchannel, add=False)

    def send_umsg(self, wid, target):
        """
        """

        data = wid.get()
        self.xstr.append(H1 % (self.server.irc.misc.nick, data))
        send_msg(self.server.irc.con, target, data)
        wid.delete(0, 'end')

class ServerController(Plugin):
    def __init__(self, xstr, irc):
        super().__init__(xstr)
        self.irc = irc

        irc.con.add_map('*JOIN', self.e_mejoin)
        irc.con.add_map('PMSG', self.e_pmsg)

        irc.con.add_map('376', lambda con, *args: 
        send_cmd(self.irc.con, self.irc.irccmd))

        irc.con.add_map('376', self.auto_join)
        irc.con.add_map('NICK', self.e_nick)
        irc.con.add_map('QUIT', self.e_quit)

        irc.con.add_map('PING', lambda con, prefix, servaddr: 
        send_cmd(irc.con, 'PONG :%s' % servaddr))

        send_cmd(irc.con, 'NICK %s' % self.irc.nick)
        send_cmd(irc.con, 'USER %s' % self.irc.user) 
        self.chmode(Extra)

        self.add_kmap(EsircNS, Main, '<Destroy>', 
        lambda event: send_cmd(irc.con, 'QUIT :escs rules!'), True)

        self.add_kmap(EsircNS, Extra, '<Key-e>', 
        self.send_cmd, add=False)

        self.add_kmap(EsircNS, Extra, '<Key-M>',  
        self.open_pchannel, add=False)

        self.ccontrollers = []
        self.pcontrollers = {}

    def auto_join(self, con, *args):
        for ind in self.irc.channels:
            send_cmd(con, 'JOIN %s' % ind)

    def e_quit(self, con, nick, user, host, msg=''):
        for ind in self.ccontrollers:
            if nick in ind.peers:
                ind.update_quit(nick, user, host, msg)

    def e_mejoin(self, con, chan):
        xstr = root.note.create(chan)
        ChannelController(xstr, self, chan)

    def create_pchannel(self, nick):
        xstr = root.note.create(nick)
        pcontroller = PMsgController(xstr, self, nick)
        return pcontroller

    def e_pmsg(self, con, nick, user, host, target, msg):
        """
        Private messages sent to the user are handled here.
        """

        pcontroller = self.pcontrollers.get(nick.lower())

        if pcontroller is None:
            pcontroller = self.create_pchannel(nick)
        pcontroller.xstr.append(H1 % (nick, msg))

    def e_nick(self, con, nicka, user, host, nickb):
        for ind in self.ccontrollers:
            if nicka in ind.peers:
                ind.update_nick(nicka, nickb)

    def send_cmd(self, event):
        """
        Used to drop irc commands.
        """

        scan = Scan()
        send_cmd(self.irc.con, scan.data)

    def open_pchannel(self, event):
        scan = Scan()
        xstr = root.note.create(scan.data)
        PMsgController(xstr, self, scan.data)

class IrcConnect:
    """
    Controls basic irc events and installs basic commands.
    """

    confs = {
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
        con.add_map(CONNECT_ERR, self.on_connect_err)
        self.misc     = None
        self.addr     = addr
        self.port     = port
        self.user     = user
        self.nick     = nick
        self.irccmd   = irccmd
        self.channels = channels
        self.encoding = encoding

    @classmethod
    def c_appearence(cls, confs):
        cls.confs.update(confs)

    def on_connect(self, con):
        xstr = root.note.create(self.addr)

        SockWriter(con)
        SockReader(con)
        Terminator(con)
        Irc(con)
        self.misc = Misc(con)
        scontroller = ServerController(xstr, self)

        con.add_map(CLOSE, lambda con, err: lose(con))

        con.add_map(Terminator.FOUND, 
        lambda con, data: xstr.append('%s\n' % data.decode(self.encoding)))

    def on_connect_err(self, con, err):
        print('esirc - Connection error: %s' % err)

