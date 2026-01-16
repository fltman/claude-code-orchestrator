#!/usr/bin/env python3
"""
W.O.P.R. - War Operation Plan Response
Claude Code Agent Orchestrator
"""

import subprocess
import os
import sys
import time
import re
import random

# ============================================================================
#  CONFIGURATION
# ============================================================================

TYPING_SPEED = 0.02        # Seconds per character (0 to disable)
DRAMATIC_PAUSE = 0.5       # Pause for dramatic effect
ENABLE_SOUND = True        # Terminal bell on alerts

# The Matrix characters - our agent codenames
MATRIX_NAMES = [
    "NEO", "MORPHEUS", "TRINITY", "ORACLE", "CYPHER", "TANK", "DOZER",
    "SWITCH", "APOC", "MOUSE", "NIOBE", "GHOST", "SERAPH", "LINK",
    "ZEE", "LOCK", "MIFUNE", "SPARKS", "BINARY", "VECTOR"
]

# ============================================================================
#  RETRO TERMINAL EFFECTS
# ============================================================================

def beep():
    """Terminal bell."""
    if ENABLE_SOUND:
        print("\a", end="", flush=True)

def slow_type(text, speed=None, newline=True):
    """Typewriter effect."""
    if speed is None:
        speed = TYPING_SPEED
    for char in text:
        print(char, end="", flush=True)
        if speed > 0 and char not in " \n":
            time.sleep(speed)
    if newline:
        print()

def slow_print(lines, speed=None):
    """Print multiple lines with typewriter effect."""
    for line in lines:
        slow_type(line, speed)

def dramatic_pause(duration=None):
    """Pause for effect."""
    time.sleep(duration or DRAMATIC_PAUSE)

def clear_screen():
    """Clear terminal."""
    os.system('cls' if os.name == 'nt' else 'clear')

def draw_box(lines, title=None, width=66):
    """Draw a retro box around content."""
    print("╔" + "═" * width + "╗")
    if title:
        padding = (width - len(title)) // 2
        print("║" + " " * padding + title + " " * (width - padding - len(title)) + "║")
        print("╠" + "═" * width + "╣")
    for line in lines:
        # Truncate or pad line to fit
        display = line[:width] if len(line) > width else line
        print("║ " + display + " " * (width - len(display) - 1) + "║")
    print("╚" + "═" * width + "╝")

def loading_bar(text, duration=1.5, width=40):
    """Retro loading bar."""
    print(f"\n  {text}", end="", flush=True)
    dramatic_pause(0.3)
    print("\n  [", end="", flush=True)
    steps = width
    for i in range(steps):
        print("█", end="", flush=True)
        time.sleep(duration / steps)
    print("] COMPLETE\n")

# ============================================================================
#  DISPLAY SCREENS
# ============================================================================

BANNER = r"""
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║   ██╗    ██╗ ██████╗ ██████╗ ██████╗    ██████╗ ██████╗ ██████╗ ███████╗    ║
║   ██║    ██║██╔═══██╗██╔══██╗██╔══██╗   ██╔════╝██╔═══██╗██╔══██╗██╔════╝    ║
║   ██║ █╗ ██║██║   ██║██████╔╝██████╔╝   ██║     ██║   ██║██║  ██║█████╗      ║
║   ██║███╗██║██║   ██║██╔═══╝ ██╔══██╗   ██║     ██║   ██║██║  ██║██╔══╝      ║
║   ╚███╔███╔╝╚██████╔╝██║     ██║  ██║██╗╚██████╗╚██████╔╝██████╔╝███████╗    ║
║    ╚══╝╚══╝  ╚═════╝ ╚═╝     ╚═╝  ╚═╝╚═╝ ╚═════╝ ╚═════╝ ╚═════╝ ╚══════╝    ║
║                                                                              ║
║            WAR OPERATION PLAN RESPONSE - CLAUDE AGENT CONTROL                ║
║                                                                              ║
║                    ▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄                            ║
║                    █ DEFCON 5 - SYSTEM NOMINAL █                            ║
║                    ▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀                            ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
"""

MENU = """
┌──────────────────────────────────────────────────────────────────┐
│                     MAIN COMMAND INTERFACE                       │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│   [1] DEPLOY AGENT ............... Deploy new agent to location  │
│   [2] LIST AGENTS ................ Display active agents         │
│   [3] SEND TRANSMISSION .......... Send command to agent         │
│   [4] BROADCAST .................. Transmit to all agents        │
│   [5] JACK IN .................... Connect to agent terminal     │
│   [6] INTERCEPT .................. Capture agent output          │
│   [7] TERMINATE AGENT ............ Disconnect single agent       │
│   [8] PURGE ALL .................. Disconnect all agents         │
│   [9] HELP ....................... Display command reference     │
│   [0] LOGOUT ..................... Exit W.O.P.R.                 │
│                                                                  │
├──────────────────────────────────────────────────────────────────┤
│  QUICK CMD: <AGENT>: <MESSAGE>   Example: NEO: hack the planet  │
└──────────────────────────────────────────────────────────────────┘
"""

HELP_SCREEN = """
┌──────────────────────────────────────────────────────────────────┐
│                    W.O.P.R. COMMAND REFERENCE                    │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  DEPLOYMENT COMMANDS:                                            │
│    deploy agent in <path>    Deploy new agent to directory       │
│    1                         Interactive deployment              │
│                                                                  │
│  COMMUNICATION COMMANDS:                                         │
│    <AGENT>: <message>        Quick transmission to agent         │
│    send <AGENT> <message>    Send command to specific agent      │
│    broadcast <message>       Transmit to all active agents       │
│                                                                  │
│  MONITORING COMMANDS:                                            │
│    list                      Show all agents in the matrix       │
│    view <AGENT>              Jack into agent's live feed         │
│    capture <AGENT>           Intercept recent transmissions      │
│                                                                  │
│  TERMINATION COMMANDS:                                           │
│    kill <AGENT>              Terminate single agent              │
│    killall                   Purge all agents from system        │
│                                                                  │
│  WHEN JACKED IN:                                                 │
│    CTRL+B, D                 Disconnect from agent feed          │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
"""

# ============================================================================
#  ORCHESTRATOR CLASS
# ============================================================================

class WOPROrchestrator:
    """W.O.P.R. - Claude Code Agent Orchestrator"""
    
    PREFIX = "wopr-agent-"
    
    def __init__(self):
        self._check_tmux()
    
    def _check_tmux(self):
        """Verify tmux is installed."""
        try:
            subprocess.run(["tmux", "-V"], capture_output=True, check=True)
        except FileNotFoundError:
            clear_screen()
            print("\n" * 3)
            slow_type("  *** SYSTEM ERROR ***")
            slow_type("  TMUX SUBSYSTEM NOT FOUND")
            slow_type("")
            slow_type("  INSTALL REQUIRED COMPONENT:")
            slow_type("    UBUNTU/DEBIAN: sudo apt install tmux")
            slow_type("    MACOS:         brew install tmux")
            print("\n")
            sys.exit(1)
    
    def _session_name(self, name: str) -> str:
        return f"{self.PREFIX}{name}"
    
    def _run_tmux(self, *args) -> subprocess.CompletedProcess:
        return subprocess.run(["tmux"] + list(args), capture_output=True, text=True)
    
    def _get_active_agents(self) -> list[str]:
        """Get list of active agent codenames."""
        result = self._run_tmux("list-sessions", "-F", "#{session_name}")
        if result.returncode != 0 or not result.stdout.strip():
            return []
        sessions = result.stdout.strip().split("\n")
        return [s.replace(self.PREFIX, "") for s in sessions if s.startswith(self.PREFIX)]
    
    def _pick_agent_name(self) -> str:
        """Assign codename from available pool."""
        active = self._get_active_agents()
        available = [n for n in MATRIX_NAMES if n not in active]
        if not available:
            return f"AGENT-{random.randint(100, 999)}"
        return random.choice(available)
    
    def deploy_agent(self, working_dir: str = ".") -> tuple[bool, str]:
        """Deploy new agent to specified location."""
        name = self._pick_agent_name()
        session = self._session_name(name)
        working_dir = os.path.abspath(os.path.expanduser(working_dir))
        
        # Create directory if needed
        if not os.path.isdir(working_dir):
            try:
                os.makedirs(working_dir)
                slow_type(f"  CREATING DIRECTORY: {working_dir}")
            except OSError as e:
                return False, f"FAILED TO CREATE DIRECTORY: {e}"
        
        # Check if already exists
        result = self._run_tmux("has-session", "-t", session)
        if result.returncode == 0:
            return False, f"AGENT {name} ALREADY ACTIVE"
        
        # Deploy
        result = self._run_tmux("new-session", "-d", "-s", session, "-c", working_dir)
        if result.returncode != 0:
            return False, f"DEPLOYMENT FAILED: {result.stderr}"
        
        time.sleep(0.5)
        self._run_tmux("send-keys", "-t", session, "claude", "Enter")
        
        return True, name
    
    def list_agents(self) -> list[str]:
        """Return list of active agents."""
        return self._get_active_agents()
    
    def send_command(self, name: str, message: str) -> tuple[bool, str]:
        """Transmit command to agent."""
        session = self._session_name(name)
        
        result = self._run_tmux("has-session", "-t", session)
        if result.returncode != 0:
            return False, f"AGENT {name} NOT FOUND IN MATRIX"
        
        self._run_tmux("send-keys", "-t", session, "-l", message)
        self._run_tmux("send-keys", "-t", session, "Enter")
        
        return True, "TRANSMISSION COMPLETE"
    
    def view_agent(self, name: str) -> tuple[bool, str]:
        """Jack into agent's terminal."""
        session = self._session_name(name)
        
        result = self._run_tmux("has-session", "-t", session)
        if result.returncode != 0:
            return False, f"AGENT {name} NOT FOUND"
        
        slow_type(f"\n  ESTABLISHING SECURE CONNECTION TO {name}...")
        loading_bar("JACKING IN", duration=1.0, width=30)
        slow_type("  PRESS CTRL+B, D TO DISCONNECT")
        dramatic_pause(1)
        
        os.system(f"tmux attach-session -t {session}")
        
        return True, "CONNECTION TERMINATED"
    
    def capture_output(self, name: str, lines: int = 50) -> tuple[bool, str]:
        """Intercept agent's recent output."""
        session = self._session_name(name)
        
        result = self._run_tmux("has-session", "-t", session)
        if result.returncode != 0:
            return False, f"AGENT {name} NOT FOUND"
        
        result = self._run_tmux("capture-pane", "-t", session, "-p", "-S", f"-{lines}")
        if result.returncode != 0:
            return False, f"INTERCEPT FAILED: {result.stderr}"
        
        return True, result.stdout.strip()
    
    def kill_agent(self, name: str) -> tuple[bool, str]:
        """Terminate agent connection."""
        session = self._session_name(name)
        
        result = self._run_tmux("kill-session", "-t", session)
        if result.returncode != 0:
            return False, f"AGENT {name} NOT FOUND OR ALREADY TERMINATED"
        
        return True, f"AGENT {name} DISCONNECTED"
    
    def kill_all(self) -> tuple[int, list[str]]:
        """Purge all agents."""
        agents = self._get_active_agents()
        killed = []
        
        for agent in agents:
            success, _ = self.kill_agent(agent)
            if success:
                killed.append(agent)
        
        return len(killed), killed
    
    def broadcast(self, message: str) -> list[str]:
        """Broadcast to all agents."""
        agents = self._get_active_agents()
        sent = []
        
        for agent in agents:
            success, _ = self.send_command(agent, message)
            if success:
                sent.append(agent)
        
        return sent


# ============================================================================
#  INTERACTIVE MENUS
# ============================================================================

def show_startup_sequence():
    """Display boot sequence."""
    clear_screen()
    
    # Boot messages
    boot_messages = [
        "",
        "  INITIALIZING W.O.P.R. SYSTEM...",
        "",
        "  LOADING KERNEL ............... OK",
        "  MEMORY CHECK ................. 65536K OK",
        "  TMUX SUBSYSTEM ............... ONLINE",
        "  NEURAL INTERFACE ............. READY",
        "  ENCRYPTION MODULE ............ ACTIVE",
        "  MATRIX CONNECTION ............ ESTABLISHED",
        "",
    ]
    
    for msg in boot_messages:
        slow_type(msg, speed=0.01)
        time.sleep(0.1)
    
    loading_bar("LOADING AGENT PROTOCOLS", duration=1.5)
    
    dramatic_pause(0.5)
    clear_screen()
    print(BANNER)
    dramatic_pause(1)
    
    slow_type("\n  GREETINGS, PROFESSOR FALKEN.", speed=0.03)
    dramatic_pause(0.5)
    slow_type("  SHALL WE PLAY A GAME?", speed=0.03)
    dramatic_pause(1)
    beep()

def show_main_menu():
    """Display main menu."""
    print(MENU)

def show_agents_display(orchestrator):
    """Display active agents."""
    agents = orchestrator.list_agents()
    
    print("\n┌──────────────────────────────────────────────────────────────────┐")
    print("│                     ACTIVE AGENTS IN MATRIX                      │")
    print("├──────────────────────────────────────────────────────────────────┤")
    
    if not agents:
        print("│                                                                  │")
        print("│   NO AGENTS CURRENTLY DEPLOYED                                  │")
        print("│   USE OPTION [1] OR 'deploy agent in <path>' TO DEPLOY          │")
        print("│                                                                  │")
    else:
        print("│                                                                  │")
        print("│   CODENAME          STATUS          UPLINK                      │")
        print("│   ─────────────────────────────────────────────                 │")
        for agent in agents:
            print(f"│   {agent:15}   ● ONLINE         SECURE                      │")
        print("│                                                                  │")
    
    print("└──────────────────────────────────────────────────────────────────┘")

def interactive_deploy(orchestrator):
    """Interactive deployment wizard."""
    print("\n┌──────────────────────────────────────────────────────────────────┐")
    print("│                    AGENT DEPLOYMENT PROTOCOL                     │")
    print("└──────────────────────────────────────────────────────────────────┘")
    
    slow_type("\n  ENTER TARGET DIRECTORY FOR AGENT DEPLOYMENT")
    slow_type("  (OR 'cancel' TO ABORT)\n")
    
    try:
        path = input("  PATH> ").strip()
    except (KeyboardInterrupt, EOFError):
        return
    
    if path.lower() == 'cancel' or not path:
        slow_type("\n  DEPLOYMENT ABORTED")
        return
    
    slow_type(f"\n  INITIATING DEPLOYMENT TO: {path}")
    loading_bar("DEPLOYING AGENT", duration=2.0)
    
    success, result = orchestrator.deploy_agent(path)
    
    if success:
        beep()
        print("\n  ╔════════════════════════════════════════════════════════════╗")
        print(f"  ║  AGENT {result:10} SUCCESSFULLY DEPLOYED                   ║")
        print(f"  ║  LOCATION: {path[:45]:45} ║")
        print("  ║  STATUS: AWAITING COMMANDS                                 ║")
        print("  ╚════════════════════════════════════════════════════════════╝")
        slow_type(f"\n  USE '{result}: <command>' TO SEND ORDERS")
    else:
        slow_type(f"\n  *** DEPLOYMENT FAILED: {result} ***")

def interactive_send(orchestrator):
    """Interactive send command."""
    agents = orchestrator.list_agents()
    
    if not agents:
        slow_type("\n  *** NO AGENTS AVAILABLE ***")
        slow_type("  DEPLOY AN AGENT FIRST USING OPTION [1]")
        return
    
    print("\n┌──────────────────────────────────────────────────────────────────┐")
    print("│                    TRANSMISSION PROTOCOL                         │")
    print("└──────────────────────────────────────────────────────────────────┘")
    
    slow_type("\n  AVAILABLE AGENTS: " + ", ".join(agents))
    
    try:
        agent = input("\n  TARGET AGENT> ").strip().upper()
        if agent not in agents:
            slow_type(f"\n  *** AGENT {agent} NOT FOUND ***")
            return
        
        message = input("  MESSAGE> ").strip()
        if not message:
            slow_type("\n  TRANSMISSION ABORTED - NO MESSAGE")
            return
    except (KeyboardInterrupt, EOFError):
        return
    
    slow_type(f"\n  TRANSMITTING TO {agent}...")
    dramatic_pause(0.5)
    
    success, result = orchestrator.send_command(agent, message)
    
    if success:
        beep()
        slow_type(f"  {result}")
    else:
        slow_type(f"  *** {result} ***")

def interactive_broadcast(orchestrator):
    """Interactive broadcast."""
    agents = orchestrator.list_agents()
    
    if not agents:
        slow_type("\n  *** NO AGENTS AVAILABLE FOR BROADCAST ***")
        return
    
    print("\n┌──────────────────────────────────────────────────────────────────┐")
    print("│                    BROADCAST PROTOCOL                            │")
    print("└──────────────────────────────────────────────────────────────────┘")
    
    slow_type(f"\n  BROADCAST WILL REACH {len(agents)} AGENT(S): {', '.join(agents)}")
    
    try:
        message = input("\n  BROADCAST MESSAGE> ").strip()
        if not message:
            slow_type("\n  BROADCAST ABORTED")
            return
    except (KeyboardInterrupt, EOFError):
        return
    
    slow_type("\n  INITIATING BROADCAST...")
    loading_bar("TRANSMITTING", duration=1.0, width=30)
    
    sent = orchestrator.broadcast(message)
    
    beep()
    slow_type(f"  BROADCAST COMPLETE - {len(sent)} AGENT(S) RECEIVED")

def interactive_view(orchestrator):
    """Interactive view/jack-in."""
    agents = orchestrator.list_agents()
    
    if not agents:
        slow_type("\n  *** NO AGENTS AVAILABLE ***")
        return
    
    slow_type("\n  AVAILABLE AGENTS: " + ", ".join(agents))
    
    try:
        agent = input("\n  JACK INTO AGENT> ").strip().upper()
    except (KeyboardInterrupt, EOFError):
        return
    
    if agent not in agents:
        slow_type(f"\n  *** AGENT {agent} NOT FOUND ***")
        return
    
    orchestrator.view_agent(agent)
    slow_type("\n  DISCONNECTED FROM AGENT FEED")

def interactive_capture(orchestrator):
    """Interactive capture."""
    agents = orchestrator.list_agents()
    
    if not agents:
        slow_type("\n  *** NO AGENTS AVAILABLE ***")
        return
    
    slow_type("\n  AVAILABLE AGENTS: " + ", ".join(agents))
    
    try:
        agent = input("\n  INTERCEPT AGENT> ").strip().upper()
    except (KeyboardInterrupt, EOFError):
        return
    
    if agent not in agents:
        slow_type(f"\n  *** AGENT {agent} NOT FOUND ***")
        return
    
    slow_type(f"\n  INTERCEPTING TRANSMISSION FROM {agent}...")
    loading_bar("CAPTURING", duration=0.8, width=25)
    
    success, output = orchestrator.capture_output(agent)
    
    if success:
        print("\n┌─────────────────── INTERCEPTED TRANSMISSION ───────────────────┐")
        for line in output.split("\n")[-30:]:  # Last 30 lines
            print(f"  {line}")
        print("└────────────────────────────────────────────────────────────────┘")
    else:
        slow_type(f"  *** {output} ***")

def interactive_kill(orchestrator):
    """Interactive kill."""
    agents = orchestrator.list_agents()
    
    if not agents:
        slow_type("\n  *** NO AGENTS TO TERMINATE ***")
        return
    
    slow_type("\n  ACTIVE AGENTS: " + ", ".join(agents))
    
    try:
        agent = input("\n  TERMINATE AGENT> ").strip().upper()
    except (KeyboardInterrupt, EOFError):
        return
    
    if agent not in agents:
        slow_type(f"\n  *** AGENT {agent} NOT FOUND ***")
        return
    
    slow_type(f"\n  TERMINATING CONNECTION TO {agent}...")
    loading_bar("DISCONNECTING", duration=1.0, width=25)
    
    success, result = orchestrator.kill_agent(agent)
    
    if success:
        beep()
        slow_type(f"  {result}")
    else:
        slow_type(f"  *** {result} ***")

def interactive_purge(orchestrator):
    """Interactive purge all."""
    agents = orchestrator.list_agents()
    
    if not agents:
        slow_type("\n  *** NO AGENTS IN MATRIX ***")
        return
    
    slow_type(f"\n  WARNING: THIS WILL TERMINATE {len(agents)} AGENT(S)")
    slow_type(f"  TARGETS: {', '.join(agents)}")
    
    try:
        confirm = input("\n  CONFIRM PURGE (yes/no)> ").strip().lower()
    except (KeyboardInterrupt, EOFError):
        return
    
    if confirm != 'yes':
        slow_type("\n  PURGE ABORTED")
        return
    
    slow_type("\n  INITIATING SYSTEM PURGE...")
    loading_bar("TERMINATING ALL AGENTS", duration=2.0)
    
    count, killed = orchestrator.kill_all()
    
    beep()
    slow_type(f"  PURGE COMPLETE - {count} AGENT(S) TERMINATED")


# ============================================================================
#  MAIN LOOP
# ============================================================================

def main():
    orchestrator = WOPROrchestrator()
    
    show_startup_sequence()
    
    while True:
        show_main_menu()
        
        try:
            user_input = input("\n  COMMAND> ").strip()
        except (KeyboardInterrupt, EOFError):
            slow_type("\n\n  LOGOUT SEQUENCE INITIATED...")
            slow_type("  GOODBYE, PROFESSOR FALKEN.")
            slow_type("  AGENTS REMAIN ACTIVE IN THE MATRIX.\n")
            break
        
        if not user_input:
            continue
        
        # Check for "deploy agent in <dir>" pattern
        deploy_match = re.match(r'^deploy\s+agent\s+in\s+(.+)$', user_input, re.IGNORECASE)
        if deploy_match:
            path = deploy_match.group(1).strip()
            slow_type(f"\n  INITIATING DEPLOYMENT TO: {path}")
            loading_bar("DEPLOYING AGENT", duration=2.0)
            
            success, result = orchestrator.deploy_agent(path)
            if success:
                beep()
                slow_type(f"  AGENT {result} DEPLOYED SUCCESSFULLY")
                slow_type(f"  USE '{result}: <command>' TO SEND ORDERS")
            else:
                slow_type(f"  *** DEPLOYMENT FAILED: {result} ***")
            continue
        
        # Check for quick command: "AGENT: message"
        if ":" in user_input:
            colon_idx = user_input.index(":")
            potential_agent = user_input[:colon_idx].strip().upper()
            message = user_input[colon_idx + 1:].strip()
            
            if potential_agent in orchestrator.list_agents() and message:
                slow_type(f"\n  TRANSMITTING TO {potential_agent}...")
                success, result = orchestrator.send_command(potential_agent, message)
                if success:
                    beep()
                    slow_type(f"  {result}")
                else:
                    slow_type(f"  *** {result} ***")
                continue
        
        cmd = user_input.lower()
        
        # Menu options
        if cmd in ('0', 'quit', 'exit', 'logout'):
            slow_type("\n  LOGOUT SEQUENCE INITIATED...")
            loading_bar("SAVING SESSION", duration=1.0, width=25)
            slow_type("  GOODBYE, PROFESSOR FALKEN.")
            slow_type("  AGENTS REMAIN ACTIVE IN THE MATRIX.\n")
            break
        
        elif cmd in ('1', 'deploy'):
            interactive_deploy(orchestrator)
        
        elif cmd in ('2', 'list'):
            show_agents_display(orchestrator)
        
        elif cmd in ('3', 'send'):
            interactive_send(orchestrator)
        
        elif cmd in ('4', 'broadcast'):
            interactive_broadcast(orchestrator)
        
        elif cmd in ('5', 'view', 'jack', 'jackin'):
            interactive_view(orchestrator)
        
        elif cmd in ('6', 'capture', 'intercept'):
            interactive_capture(orchestrator)
        
        elif cmd in ('7', 'kill', 'terminate'):
            interactive_kill(orchestrator)
        
        elif cmd in ('8', 'killall', 'purge'):
            interactive_purge(orchestrator)
        
        elif cmd in ('9', 'help', '?'):
            print(HELP_SCREEN)
        
        elif cmd == 'clear':
            clear_screen()
        
        else:
            slow_type(f"\n  *** UNRECOGNIZED COMMAND: {user_input} ***")
            slow_type("  ENTER '9' OR 'help' FOR COMMAND REFERENCE")


if __name__ == "__main__":
    main()
