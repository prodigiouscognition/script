import streamlit as st
import pandas as pd
import plotly.express as px
from modules import BulletEngine, ScriptAudit

# --- 1. SCRIPT DATABASE ---
SCRIPTS = {
    "--- Choose a Script ---": "",

    "John":
    """**SCENE 1**
    
    **INT. BEDROOM - DAY**
    
    JOHN PROTAGONIST (25, very handsome with blue eyes and a muscular build that shows he works out) wakes up. He looks in the mirror and talks to himself so the audience knows who he is.
    
    **JOHN**
    (to the mirror)
    Well, John, today is the day. Since my parents died in that mysterious fire ten years ago that the police never solved, I have been waiting to find the Orb of Dark Destiny. I am a lonely loner who doesn't need anyone, except for my best friend who is about to walk in.
    
    **BEST FRIEND** walks in. His name is BILL. He is wearing a shirt that says "I AM THE COMIC RELIEF."
    
    **BILL**
    Hey John! As you know, we are both graduates of the Space Academy where we learned how to fly ships and also how to fight with lasers. Are you ready for our mission to the Planet of Doom?
    
    **JOHN**
    I am ready, Bill. But first, I must feel an emotion. 
    
    John looks at a photo of a woman. 
    
    **JOHN**
    I miss my wife. She was so beautiful before the aliens took her.
    
    **BILL**
    That is sad. But look! An explosion!
    
    **EXT. SPACE - CONTINUOUS**
    
    A giant explosion happens in space. It is very loud, even though there is no sound in space, but the characters hear it anyway. 
    
    **BILL**
    Oh no! The villains are here! It is the Evil Emperor Malice!
    
    **INT. EVIL SHIP - SAME TIME**
    
    **EMPEROR MALICE** sits on a throne made of skulls. He looks at the camera.
    
    **EMPEROR MALICE**
    I am evil! I will find the Orb and then I will rule the galaxy because I want to be in charge of everything. Guards! Execute Plan Alpha-Beta-9 because that is the plan that is bad for the heroes!
    
    **SCENE 2**
    
    **INT. THE PLANET OF DOOM - TEN MINUTES LATER**
    
    John and Bill are already there. They didn't have to travel. They are just there now.
    
    **JOHN**
    Wait, I see the Orb. It is right there on that pedestal that isn't guarded by anyone.
    
    **BILL**
    Wow, that was easy. I hope nothing ironic happens.
    
    Suddenly, a giant robot falls from the ceiling. 
    
    **ROBOT**
    I AM A ROBOT. I WILL KILL YOU NOW.
    
    **JOHN**
    Not if I use my secret power that I never mentioned until this exact second!
    
    John glows bright green. The robot explodes instantly.
    
    **BILL**
    Wow, John. You are the chosen one.
    
    **JOHN**
    I know. Let’s go get lunch.
    
    **FADE OUT.**
    
    **THE END.**""",

    "The Abyss-7 ": """Title: THE ABYSS-7 PROTOCOL
    Characters: 
    DR. ARIS (50s, weary, hiding a secret)
    LEO (20s, nervous, high-strung technician)

    [SCENE 1: THE CONTROL ROOM]
    The room is a claustrophobic cage of blinking LED arrays and ancient CRT monitors. Outside the thick reinforced glass, there is only the absolute black of the Hadal Zone.
    ARIS: (Whispering) Seventy-two hours without a sun. It changes the way your blood moves, Leo.
    LEO: (Typing frantically) My blood is moving fine. It’s the sonar that’s bleeding. Look at the return signal.
    Aris leans over. A rhythmic pulse—thump... thump... thump—echoes through the speakers.
    LEO: That’s not a whale. It’s too consistent. It’s five hundred tons of mass moving at forty knots.
    ARIS: (Coldly) It’s the Abyss-7 protocol. It was always going to wake up.
    LEO: (Stops typing) Protocol? Aris, we’re three hundred meters below the crush depth of a nuclear sub. This station is held together by hope and rusted titanium. What 'protocol' involves a leviathan circling our hull?
    ARIS: The research grant wasn't for silt, Leo. The Company wanted to know what happened to the 2021 expedition. They didn't vanish. They were harvested.
    LEO: Harvested? By what?
    ARIS: (Points to the screen) By the thing that’s currently looking for the airlock.
    """,

    "Pyaar Ka Server ": """Title: PYAAR KA SERVER: A TECH ROMANCE
    Characters: 
    RAHUL (An obsessed coder who speaks in metaphors)
    PRIYA (A woman who is tired of tech-jargon)
    SIMI (Priya’s best friend, the 'Insta-influencer' type)
    """,

    "Blood & Dust ": """Title: BLOOD & DUST
    Characters: 
    HUMAYUN (A man with a blood-stained past)
    VICKY (His younger, naive brother)
    CHAUHAN (The ruthless landlord)
    """
}


st.set_page_config(page_title="Bullet | Production Intel", layout="wide")
engine = BulletEngine()

# --- SESSION STATE ---
if "audit" not in st.session_state:
    st.session_state.audit = None

if "chat" not in st.session_state:
    st.session_state.chat = []

if "script_text" not in st.session_state:
    st.session_state.script_text = ""

if "input_source" not in st.session_state:
    st.session_state.input_source = None

st.title("🎬 Bullet: Production Intelligence Dashboard")
st.caption("Deterministic Studio Auditing with Ironclad Grounding")

# --- 2. INPUT ---
# --- 2. INPUT (REPLACE THIS SECTION) ---
c1, c2 = st.columns([3, 1])
with c1:
    # THE FIX: Explicitly choose which input the Producer should look at
    src_mode = st.radio(
        "Select Input Source:", 
        ["Sample Script", "Pasted Text", "Uploaded PDF"], 
        horizontal=True,
        help="Switching this will tell the Producer which input to ignore."
    )
    
    st.divider()
    
    final_input = ""

    if src_mode == "Sample Script":
        sel = st.selectbox("Choose from Database:", list(SCRIPTS.keys()))
        if sel != "--- Choose a Script ---":
            final_input = SCRIPTS[sel]
            st.caption("✅ Ready to audit sample script.")

    elif src_mode == "Pasted Text":
        paste = st.text_area("Paste your dialogue here:", height=200)
        if paste:
            final_input = engine.get_text(paste)
            st.caption("✅ Ready to audit pasted text.")

    elif src_mode == "Uploaded PDF":
        up = st.file_uploader("Upload a Script PDF:", type=["pdf"])
        if up:
            final_input = engine.get_text(up)
            st.caption(f"✅ Ready to audit: {up.name}")
        else:
            st.info("Please upload a PDF file to proceed.")

with c2:
    st.write("##")
    if st.button("Run Narrative Audit", type="primary", use_container_width=True):
        if final_input:
            st.session_state.chat = []
            st.session_state.audit = None
            st.session_state.script_text = final_input

            with st.spinner("Producer is auditing the DNA..."):
                try:
                    res = engine.analyze(st.session_state.script_text)
                    st.session_state.audit = ScriptAudit(**res)
                except Exception as e:
                    st.error(f"Audit Error: {e}")

# --- 3. REPORT ---
if st.session_state.audit:
    data = st.session_state.audit

    if not data.is_narrative:
        st.error(f"🚨 REJECTED: Not a story. Reason: {data.rejection_reason}")

    elif not data.is_presentable:
        st.warning(f"⚠️ ZERO SCORE: Content is too short or nonsensical.")
        st.info(f"Producer's Note: {data.rejection_reason}")

    else:
        st.divider()
        st.info(f"📊 **Market Fit Analysis:** {data.market_benchmark_reason}")
        st.success(f"👥 **Audience Analysis:** {data.audience_demographic}")

        k1, k2, k3 = st.columns(3)
        k1.metric("Engagement Score", f"{data.engagement_score}%")
        k2.metric("Hook Quality", f"{data.hook.score}%")
        k3.metric("Dialogue Depth", f"{data.dialogue.score}%")

        tabs = st.tabs(["📊 Scene Audit", "👥 Character Map", "🔧 Script Doctor", "💬 Chat"])

        # Scene Audit
        with tabs[0]:
            if data.scenes:
                beat_df = pd.DataFrame(
                    [{"Scene": s.title, "Tension": s.tension} for s in data.scenes]
                )
                st.plotly_chart(
                    px.line(beat_df, x="Scene", y="Tension", markers=True, range_y=[0, 100]),
                    use_container_width=True
                )

                for s in data.scenes:
                    with st.expander(f"{s.title} ({s.emotional_shift})"):
                        st.info(f"**Doctor Note:** {s.script_doctor_note}")

        # Character Map
        with tabs[1]:
            for char in data.characters:
                cll, clr = st.columns([1, 2])
                cll.markdown(f"**{char.name}** ({char.archetype})")
                clr.write(f"**Motivation:** {char.motivation}")
                clr.write(f"**Fatal Flaw:** {char.fatal_flaw}")
                clr.success(f"**Market Potential:** {char.market_potential}")
                st.divider()

        # Script Doctor
        with tabs[2]:
            st.subheader("Retention Analysis: Cliffhangers")
            for cf in data.cliffhangers:
                st.markdown(f"> \"*{cf.line}*\"")
                st.caption(f"**Logic:** {cf.logic}")
                st.divider()

            st.subheader("Critical Improvements")
            for imp in data.improvements:
                st.write(f"👉 {imp}")

        # Chat
        with tabs[3]:
            chat_container = st.container(height=300)
            with chat_container:
                for m in st.session_state.chat:
                    with st.chat_message(m["role"]):
                        st.write(m["content"])

            if p := st.chat_input("Ask the Producer..."):
                st.session_state.chat.append({"role": "user", "content": p})
                ans = engine.chat_grounded(
                    p,
                    st.session_state.script_text,
                    st.session_state.chat[:-1]
                )
                st.session_state.chat.append({"role": "assistant", "content": ans})
                st.rerun()