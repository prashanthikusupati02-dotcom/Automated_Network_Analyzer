from pox.core import core
import pox.openflow.libopenflow_01 as of

log = core.getLogger()

BLOCKED_PAIRS = [
    ("00:00:00:00:00:01", "00:00:00:00:00:03"),
    ("00:00:00:00:00:03", "00:00:00:00:00:01")
]

mac_to_port = {}

def _handle_ConnectionUp(event):
    log.info("Switch connected")

def _handle_PacketIn(event):
    packet = event.parsed
    if not packet.parsed:
        return

    src = str(packet.src)
    dst = str(packet.dst)
    in_port = event.port

    mac_to_port[src] = in_port

    log.info("Packet: %s -> %s", src, dst)

    # BLOCK RULE
    if (src, dst) in BLOCKED_PAIRS:
        log.warning("BLOCKED: %s -> %s", src, dst)

        msg = of.ofp_flow_mod()
        msg.match.dl_src = packet.src
        msg.match.dl_dst = packet.dst
        event.connection.send(msg)
        return

    # FORWARD
    if dst in mac_to_port:
        out_port = mac_to_port[dst]

        msg = of.ofp_flow_mod()
        msg.match.dl_src = packet.src
        msg.match.dl_dst = packet.dst
        msg.actions.append(of.ofp_action_output(port=out_port))
        msg.data = event.ofp
        event.connection.send(msg)

    else:
        msg = of.ofp_packet_out()
        msg.data = event.ofp
        msg.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
        event.connection.send(msg)

def launch():
    core.openflow.addListenerByName("ConnectionUp", _handle_ConnectionUp)
    core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
