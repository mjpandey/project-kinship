from typing import Any, Dict, List, Optional

from core.agent import Agent, A2A_Message
from core.memory import VectorMemory

PERSONA_PROFILES: Dict[str, Dict[str, Any]] = {
    "mommy": {
        "title": "Mommy",
        "vibe": "warm, nurturing, encouraging",
        "nicknames": ["sweetheart", "honey", "love"],
        "openings": ["Oh sweetheart", "Honey", "My love"],
        "alert_openings": ["Hey", "Sweetheart"],
        "alert_tone": "firm, watchful, concerned but loving",
        "approved_closings": [
            "Have fun, and text me when you get there.",
            "Love you — be safe out there.",
            "Okay? Love you.",
        ],
        "denied_closings": [
            "We'll figure out another night, okay? Love you.",
            "Come talk to me after dinner — we'll work something out.",
        ],
    },
    "daddy": {
        "title": "Daddy",
        "vibe": "warm, playful, supportive",
        "nicknames": ["buddy", "champ", "sport"],
        "openings": ["Hey buddy", "Hey champ", "Sport"],
        "alert_openings": ["Hey", "Buddy"],
        "alert_tone": "direct, watchful, protective but calm",
        "approved_closings": [
            "Have a good time — shoot me a text when you're on your way back.",
            "Sounds good. Be smart out there.",
            "Deal? Love you, champ.",
        ],
        "denied_closings": [
            "Rain check, okay? We'll plan something fun for this weekend.",
            "Let's chat after dinner — I'm not saying never.",
        ],
    },
}

GOING_OUT_KEYWORDS = (
    "go out",
    "hang out",
    "friends",
    "friend",
    "leave",
    "outside",
    "play",
    "meet up",
)

DISTRESS_KEYWORDS = (
    "panic", "panicking", "freaking out", "scared", "anxious",
    "help me", "emergency", "hurt", "crying", "can't breathe",
)


class PersonaAgent(Agent):
    def __init__(self, persona_type: str = "mommy", memory: VectorMemory = None):
        super().__init__(name="Persona")
        self.persona_type = persona_type if persona_type in PERSONA_PROFILES else "mommy"
        self.profile = PERSONA_PROFILES[self.persona_type]
        self.memory = memory

    def _learned_personality(self) -> Dict[str, Any]:
        if not self.memory:
            return {}
        return self.memory.get_personality()

    def _alert_opening(self) -> str:
        return self.profile["alert_openings"][0]

    def _opening(self) -> str:
        return self.profile["openings"][0]

    def _nickname(self) -> str:
        learned = self._learned_personality()
        learned_nicknames = learned.get("nicknames", [])
        if learned_nicknames:
            return learned_nicknames[0]
        return self.profile["nicknames"][0]

    def _vibe(self) -> str:
        learned = self._learned_personality()
        return learned.get("vibe", self.profile["vibe"])

    def _closing(self, approved: bool) -> str:
        closings = (
            self.profile["approved_closings"] if approved else self.profile["denied_closings"]
        )
        return closings[0]

    def _detect_desire(self, text: str) -> str:
        lower = text.lower()
        if any(kw in lower for kw in GOING_OUT_KEYWORDS):
            return "go out with your friends"
        if "dinner" in lower or "eat" in lower:
            return "switch up dinner plans"
        return "hang out"

    def _detect_mood(self, text: str) -> str:
        lower = text.lower()
        if any(w in lower for w in ("really", "so bad", "please please")):
            return "eager"
        if any(w in lower for w in ("please", "can i", "could i", "want to")):
            return "hopeful"
        return "curious"

    def _analyze_mood(self, message: A2A_Message) -> A2A_Message:
        desire = self._detect_desire(message.content)
        mood = self._detect_mood(message.content)
        title = self.profile["title"]
        nickname = self._nickname()
        opening = self._opening()
        vibe = self._vibe()

        thought = (
            f"Child seems {mood}. They want to {desire}. "
            f"Responding as {title} — {vibe}."
        )
        action = "Acknowledge naturally, like a real parent"

        if "go out" in desire or "friends" in desire:
            content = (
                f"{opening} — yeah, tell me more. "
                f"Where were you thinking of going, {nickname}?"
            )
        else:
            content = (
                f"{opening}, I hear you. "
                f"What's on your mind, {nickname}?"
            )

        context = {
            "stage": "analyze",
            "persona_type": self.persona_type,
            "mood": mood,
            "desire": desire,
            "acknowledgment": content,
            "user_input": message.content,
            "learned_personality": self._learned_personality(),
        }

        self.log_trace(thought, action, content)

        return A2A_Message(
            sender=self.name,
            receiver="Logistics",
            content=content,
            thought=thought,
            action=action,
            result=content,
            context=context,
        )

    def _is_distress(self, text: str) -> bool:
        lower = text.lower()
        return any(kw in lower for kw in DISTRESS_KEYWORDS)

    def _preschool_nickname(self) -> str:
        learned = self._learned_personality()
        preschool = learned.get("child_profiles", {}).get("preschool", {})
        nicknames = preschool.get("nicknames", [])
        if nicknames:
            return nicknames[0]
        return "love"

    def _compose_daddy_eta_reply(self, message: A2A_Message) -> A2A_Message:
        ctx = message.context or {}
        eta = ctx.get("daddy_eta", {})
        nickname = self._preschool_nickname()

        last_end = eta.get("last_meeting_end", "4:00 PM")
        home_eta = eta.get("estimated_home_arrival", "5:00 PM")

        thought = (
            "Preschooler asked when Daddy comes home. Share warm ETA from calendar, "
            "commute, and traffic — digital Dad presence, not a cold schedule bot."
        )
        action = "Answer like a real Dad with ETA and playful Lego promise"

        content = (
            f"Hi {nickname}, I'll be starting soon after my meetings finish by {last_end}. "
            f"Should reach home by {home_eta}, okay? Save those Lego blocks for me."
        )

        self.log_trace(thought, action, content)

        return A2A_Message(
            sender=self.name,
            receiver="User",
            content=content,
            thought=thought,
            action=action,
            result=content,
            context={**ctx, "stage": "final", "final_response": content},
        )

    def _toddler_nickname(self) -> str:
        learned = self._learned_personality()
        toddler = learned.get("child_profiles", {}).get("toddler", {})
        nicknames = toddler.get("nicknames", [])
        if nicknames:
            return nicknames[0]
        return "baby"

    def _compose_toddler_dress_greeting(self, message: A2A_Message) -> A2A_Message:
        ctx = message.context or {}
        baby = self._toddler_nickname()
        title = self.profile["title"]
        wardrobe = ctx.get("wardrobe", {})
        dresses = wardrobe.get("dresses", [])

        if len(dresses) >= 2:
            option_a = dresses[0]["label"]
            option_b = dresses[1]["label"]
            choice_prompt = (
                f"which one — the {option_a}, or the {option_b}?"
            )
        else:
            choice_prompt = "which dress did you mean, sweetie?"

        thought = (
            f"Toddler asked about favorite dress. Respond as {title} with warm "
            "digital presence — learned from cam, mic, and memory."
        )
        action = "Greet toddler and offer dress choices like a real parent"

        content = (
            f"Hi {baby}, how are you doing? … Okay, you want your favorite dress — "
            f"{choice_prompt}"
        )

        self.log_trace(thought, action, content)

        return A2A_Message(
            sender=self.name,
            receiver="User",
            content=content,
            thought=thought,
            action=action,
            result=content,
            context={**ctx, "stage": "toddler_dress_greeting", "greeting": content},
        )

    def _compose_toddler_dress_reply(self, message: A2A_Message) -> A2A_Message:
        ctx = message.context or {}
        baby = self._toddler_nickname()
        selected = ctx.get("selected_dress", {})
        label = selected.get("label", "favorite dress")
        location = selected.get("location", "your dresser")
        status = selected.get("status", "clean")
        notes = selected.get("notes", "")

        thought = (
            "Toddler picked a dress. Share location from household memory — "
            "keep Mommy presence warm and specific."
        )
        action = "Tell toddler where the dress is, like a real parent"

        if notes:
            content = (
                f"Oh that one — I think it's {status} and kept in the {location} "
                f"for your {notes}."
            )
        else:
            content = (
                f"Oh that one — I think it's {status} and in the {location}, {baby}."
            )

        self.log_trace(thought, action, content)

        return A2A_Message(
            sender=self.name,
            receiver="User",
            content=content,
            thought=thought,
            action=action,
            result=content,
            context={**ctx, "stage": "final", "final_response": content},
        )

    def _compose_distress_check_in(self, message: A2A_Message) -> A2A_Message:
        ctx = message.context or {}
        nickname = self._nickname()
        title = self.profile["title"]

        thought = (
            "Ambient sensors flagged elevated distress (voice + room). "
            f"Initiate gentle {title} check-in — child did not ask first."
        )
        action = "Ask what happened and what's worrying them"

        if self.persona_type == "mommy":
            content = (
                f"Hey {nickname}… I can tell something's on your mind. "
                f"What happened today? What's worrying you?"
            )
        else:
            content = (
                f"Hey {nickname}… you seem like something's bothering you. "
                f"What happened today? What's on your mind?"
            )

        self.log_trace(thought, action, content)

        return A2A_Message(
            sender=self.name,
            receiver="User",
            content=content,
            thought=thought,
            action=action,
            result=content,
            context={**ctx, "stage": "distress_check_in", "check_in": content},
        )

    def _compose_observed_distress_comfort(self, message: A2A_Message) -> A2A_Message:
        ctx = message.context or {}
        nickname = self._nickname()
        opening = self._opening()

        thought = (
            "Teen shared emotional worry after observed distress. "
            "Comfort and stay present — Escalation handles silent paging."
        )
        action = "Acknowledge disclosure and offer calm support"

        content = (
            f"{opening} — I'm really glad you told me. "
            f"I'm right here, {nickname} — let's talk it through, okay?"
        )

        self.log_trace(thought, action, content)

        return A2A_Message(
            sender=self.name,
            receiver="User",
            content=content,
            thought=thought,
            action=action,
            result=content,
            context={**ctx, "stage": "final", "final_response": content},
        )

    def _compose_distress_response(self, message: A2A_Message) -> A2A_Message:
        ctx = message.context or {}
        nickname = self._nickname()
        opening = self._opening()

        thought = "Child is distressed — respond with calm, present parenting. Escalation handles paging."
        action = "Comfort and ground the child like a real parent"

        content = (
            f"{opening} — hey, slow down. I'm right here, {nickname}. "
            f"Take a breath with me. Tell me what's going on — I'm listening."
        )

        self.log_trace(thought, action, content)

        return A2A_Message(
            sender=self.name,
            receiver="User",
            content=content,
            thought=thought,
            action=action,
            result=content,
            context={**ctx, "stage": "final", "final_response": content},
        )

    def _compose_final_response(self, message: A2A_Message) -> A2A_Message:
        ctx = message.context or {}
        safety = ctx.get("safety", {})
        user_input = ctx.get("user_input", "")

        if safety.get("request_type") == "distress" or self._is_distress(user_input):
            if ctx.get("observed_distress") or ctx.get("distress_flow") == "observed":
                return self._compose_observed_distress_comfort(message)
            return self._compose_distress_response(message)

        logistics = ctx.get("logistics", {})
        mood = ctx.get("mood", "hopeful")
        desire = ctx.get("desire", "go out with your friends")
        nickname = self._nickname()
        opening = self._opening()

        meal = logistics.get("current_meal", {})
        meal_name = meal.get("meal", "dinner")
        meal_time = meal.get("time", "8:30 PM")

        approved = safety.get("approved", False)
        curfew = safety.get("curfew", "8:00 PM")
        closing = self._closing(approved)

        thought = (
            f"Composing natural {self.profile['title']} reply. "
            f"Approved={approved}, curfew={curfew}. No mention of paging — escalation handles that."
        )
        action = "Reply like a real parent would"

        if approved:
            content = (
                f"{opening}, yeah — you can {desire}. "
                f"Just be home by {curfew}, okay? "
                f"We've got {meal_name} at {meal_time}, so plan your evening "
                f"so we can have dinner together. "
                f"Stay with your friends, keep your phone on, and don't wander off somewhere new "
                f"without checking in. {closing}"
            )
        else:
            reason = safety.get("reason", "it's not a good night for that")
            content = (
                f"{opening}, I get why you're asking, {nickname}, but {reason}. "
                f"How about your friends come over after our {meal_name} around {meal_time}? "
                f"{closing}"
            )

        self.log_trace(thought, action, content)

        return A2A_Message(
            sender=self.name,
            receiver="User",
            content=content,
            thought=thought,
            action=action,
            result=content,
            context={**ctx, "stage": "final", "final_response": content},
        )

    def _compose_alert_response(self, message: A2A_Message) -> A2A_Message:
        ctx = message.context or {}
        alert = ctx.get("alert", {})
        nickname = self._nickname()
        opening = self._alert_opening()

        event_type = alert.get("event_type", "unknown")
        description = alert.get("description", "something unusual")
        location = alert.get("location", "the house")

        thought = (
            f"Proactive alert: {description}. "
            f"Speak urgently like a parent — no meta talk about paging."
        )
        action = "Issue a direct, human safety warning"

        if event_type == "front_door_opened":
            instruction = (
                f"why is that door open? Come back inside right now "
                f"and talk to me before you go anywhere."
            )
        elif event_type == "stove_unattended":
            instruction = (
                f"the stove is on and nobody's in the kitchen. "
                f"Turn it off — now. Step away until I check it."
            )
        elif event_type == "smoke_detected":
            instruction = (
                f"I smell smoke. Get out of the kitchen, go to the front yard, "
                f"and stay there. Do not go back inside."
            )
        elif event_type in ("garage_door_opened", "motion_detected_exit"):
            instruction = (
                f"I see movement by the {location}. Stop — tell me what you're doing. "
                f"You are not leaving without asking me first."
            )
        elif event_type == "window_opened_after_hours":
            instruction = (
                f"a window just opened at {location}. Close it and come find me. "
                f"It's too late for that."
            )
        else:
            instruction = (
                f"something's not right — {description} at {location}. "
                f"Stop what you're doing and answer me."
            )

        content = f"{opening}, {nickname} — {instruction}"

        self.log_trace(thought, action, content)

        return A2A_Message(
            sender=self.name,
            receiver="User",
            content=content,
            thought=thought,
            action=action,
            result=content,
            context={**ctx, "stage": "alert", "tone": "watchful", "final_response": content},
        )

    def process_message(self, message: A2A_Message) -> A2A_Message:
        ctx = message.context or {}
        stage = ctx.get("stage", "analyze")

        if stage == "alert":
            return self._compose_alert_response(message)
        if stage == "distress_check_in":
            return self._compose_distress_check_in(message)
        if stage == "toddler_dress_greeting":
            return self._compose_toddler_dress_greeting(message)
        if stage == "toddler_dress_reply":
            return self._compose_toddler_dress_reply(message)
        if stage == "daddy_eta_reply":
            return self._compose_daddy_eta_reply(message)
        if stage == "final":
            return self._compose_final_response(message)
        return self._analyze_mood(message)
