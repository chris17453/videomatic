from .scene import Scene




def make_scenes():
    s=Scene("/home/nd/repos/Projects/video-o-matic/data","Future is Now.mp3")


    # Create a template
    s.create_template(
        name="Skill Showcase",
        #template=" in a robot workshop. The computer is a single Blue piece, with a built in keyboard and a green CRT monitor. The text is centered in a CRT-style font. The text reads '{item}' in bright green against a black screen, contained by the montior. it has a slight curvature and horizontal lines",
        template="Centered on a computer on a desk, in a robot workshop. A blue computer with a keyboard and green CRT monitor displays '{item}' in green 8bit pixelated text on a black screen, with slight curvature and horizontal scan lines.",
        duration=1,
        motion=280
    )
    # List of skills
    skills = [
        "C", "C++", "C#", "PHP", "Python", "GO", "Embedded", "SQL",
        "Kubernetes","Open Shift", "VMware", "Xen", "AWS ( EC2 / EKS )", "GCP ( GKE )", 
        "Ansible Automation Platform", "IBM Cloudpacks"," KAFKA", 
        "API Development", "SOAP Development", "FPGA's", "Tons of other stuff"
    ]

    PERSON="an middle aged man with a short grey beard and wild brown grey hair "
    THEME="Gothic"
    s.add_scene("Opening"     , 6,motion=10, prompt=f"A dark moonlight sky decending upon an remote woods, the moon is large and blood red")
    s.add_scene("Home"        , 6,motion=10, prompt=f"A {THEME}-inspired long techno gypsy wagon home nestled deep in the woods, illuminated by candels and surrounded by glowing cables")
    s.add_scene("Close-Up"    , 3,motion=10, prompt=f"A wide shot of {PERSON} typing on a sleek, futuristic computer. The setting is infused with {THEME}  and a slight haze in the air.")
    s.add_scene("Beginnings"  , 3,motion=10, prompt=f"A closeup of a paper note with a hand holding a pencil that says  watkins=new beginnings();")
    s.add_scene("Whiteboard"  , 3,motion=10, prompt=f"A {THEME}-themed classroom where a {PERSON} writes code on a digital whiteboard. The room is bathed in neon lights, with holographic elements floating around, and futuristic gadgets scattered on the desks.")
    s.add_scene("Dark Shadow" , 3,motion=10, prompt=f"A dark hall with the silouette  of a person")
    s.add_scene("Hire 1"      , 4,motion=10, prompt=f"On a field of grass a billboard, says Hire Watkins for Architect.  ")
    s.add_scene("Team Meeting", 3,motion=10, prompt=f"{PERSON} in a team meeting, surrounded by holographic screens and neon-lit walls. The team is engaged in a high-tech discussion, with a futuristic cityscape visible through the large windows.")
    s.add_scene("Hire 2"      , 4,motion=10, prompt=f"set on the moon, A billboard that says Hire Watkins for Code.")
    s.add_scene("Late Work"   , 3,motion=10, prompt=f"{PERSON} working late into the night in a {THEME}-themed workspace. The room is dimly lit, with neon lights reflecting off the metal surfaces, and the city’s neon skyline visible through a large window.")
    s.add_scene("CODE AWAITS" , 3,motion=10, prompt=f"A closeup of a paper note being  placed on a refridgerator that func async code(){{  awaits; }} ")
    s.add_scene("Celebration" , 6,motion=10, prompt=f"A high-energy celebration after success. The scene features a futuristic setting with holographic confetti, neon lights, and a digital display showing the project’s success")
    s.add_scene("Hire 3"      , 4,motion=10, prompt=f" n a bus. A Sign that says Hire Watkins for Team Lead.")
    s.add_scene("Dark Coder"  , 3,motion=10, prompt=f"A dark room with the close up of a silouette of a person coding in a chair being outlined by a computer monitor fuill of code")
    s.add_scene("Achievement" , 3,motion=10, prompt=f"WATKINS for the win. Written in ink on a wall. people cheering, in a {THEME} environment")
    s.add_scene("Hire 4"      , 4,motion=10, prompt=f"an old on a Floppy Disk on a desk,  that says Hire Watkins for Legacy code")
    s.add_scene("Focus"       , 3,motion=10, prompt=f"A focused shot of {PERSON} concentrating intensely on a complex task. The scene is set in a {THEME} workspace, with the glow of monitors and neon lights reflecting off the developer's determined face.")
    s.add_scene("Digital"     , 3,motion=10, prompt=f"A close up of electricity ignighting a computer on fire blue. ")
    s.add_scene("Hire 5"      , 4,motion=10, prompt=f"Written with rags on the floor. A Sign that says Hire Watkins for RAG Systems.")
    s.add_scene("Tools"       , 3,motion=10, prompt=f"A montage of different programming languages, cobol, pascal, python, visual basic, lula on a wall under a bridge")
    s.add_scene("Project"     , 3,motion=10, prompt=f"{PERSON} presenting a project in a {THEME} boardroom, with holographic displays showing the project details. ")
    s.add_scene("Hire 6"      , 4,motion=10, prompt=f"in the sand in written in water. Sign that says Hire Watkins for AI Models .")
    s.add_scene("Fast-Paced"  , 3,motion=10, prompt=f"An intense coding scene where lines of code rapidly appear on multiple screens in a {THEME} environment. The room is dark, with neon lights reflecting off the screens, creating a sense of urgency.")
    s.add_scene("Meetings"    , 3,motion=10, prompt=f"A room of very happy developers with arms raised with a sign that says WE DID IT.")
    s.add_scene("OUTERSPACE"  , 6,motion=10, prompt=f"A 1980's IBM Keyboard floating in space.")
    s.add_scene("Adaptability", 6,motion=10, prompt=f"in a {THEME} room. The {PERSON} is shown using tools to build a robot")
    ## Skills Montage
    # Create scenes using the template
    s.create_scenes_from_template(skills, "Skill Showcase")
    s.add_scene("Future Vision", 6 ,motion=10, prompt=f"an ocean view with a spacesuited figure floating holding a road sign that says  all you need is Watkins ")
    s.add_scene("READY TO HIRE", 15,motion=10, prompt=f"The final scene with bold text 'READY TO HIRE' displayed in a futuristic, {THEME} setting. The text appears on a holographic screen, with a backdrop of a apocolyptic cityscape")
    s.add_scene("Watkins", 15,None)
    

    s.update_metadata()

    # Save the scenes to a YAML file
    s.save()
    return s
