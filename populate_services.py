from core.models import Service

services_data = [
    {
        "title": "Musical Style",
        "icon": "bi bi-music-note-list",
        "short_description": "Classic Swing, Smooth Jazz, Afro-Jazz, Rhumba, Classical, Contemporary Pop (swing versions), Kenyan Hits.",
        "detailed_description": "We specialize in a diverse range of musical styles to suit any occasion. From the timeless elegance of Classic Swing and Smooth Jazz to the rhythmic beats of Afro-Jazz and Rhumba. We also offer Classical performances for ceremonies and unique Swing renditions of Contemporary Pop and Kenyan Hits. Our versatility ensures the perfect soundtrack for your event."
    },
    {
        "title": "Christmas Package",
        "icon": "bi bi-gift-fill",
        "short_description": "Extended Evening: Full Swing Quartet (Piano, Guitar, Clarinet, Trumpet, Saxophone). 4x45 min sets. Contact for rates.",
        "detailed_description": "Celebrate the festive season with our exclusive Christmas Package. Features a Full Swing Quartet with Piano, Guitar, Clarinet, Trumpet, and Saxophone. Enjoy up to 4 sets of 45 minutes each, filled with holiday classics and jazz standards. Perfect for corporate holiday parties, family gatherings, and festive dinners. Contact us for a customized quote."
    },
    {
        "title": "Cocktail Elegance",
        "icon": "bi bi-cup-straw",
        "short_description": "Perfect for intimate gatherings and networking events. Set the mood with smooth jazz. Contact for rates.",
        "detailed_description": "Create a sophisticated atmosphere for your cocktail hour or networking event. Our Cocktail Elegance package focuses on smooth jazz and background swing that enhances conversation without overpowering it. deal for art gallery openings, corporate mixers, and private receptions."
    },
    {
        "title": "Wedding Serenade",
        "icon": "bi bi-heart-fill",
        "short_description": "Make your special day unforgettable with romantic jazz and lively swing for the reception. Contact for rates.",
        "detailed_description": "From walking down the aisle to the first dance, our Wedding Serenade package covers it all. We provide romantic jazz instrumentals for the ceremony and lively, dance-worthy swing for the reception. We work closely with you to curate a playlist that reflects your love story."
    },
    {
        "title": "Corporate Gold",
        "icon": "bi bi-briefcase-fill",
        "short_description": "The ultimate entertainment package for high-end corporate functions and galas. Contact for rates.",
        "detailed_description": "Impress your clients and stakeholders with our Corporate Gold package. Designed for high-end galas, award ceremonies, and product launches. We deliver a polished, professional performance that aligns with your brand's prestige. Includes options for background music during dinner and upbeat sets for post-event networking."
    },
    {
        "title": "Custom Repertoire",
        "icon": "bi bi-music-player-fill",
        "short_description": "Popular Standards: Fly Me to the Moon, Sing Sing Sing. Kenyan Reimagined: Sauti Sol, Nyashinski jazz renditions.",
        "detailed_description": "Have a specific song in mind? Our Custom Repertoire service allows you to request special songs. We perform popular standards like 'Fly Me to the Moon' and 'Sing Sing Sing', as well as unique jazz reimaginations of Kenyan hits from artists like Sauti Sol and Nyashinski. Let us create a musical experience that is uniquely yours."
    }
]

for data in services_data:
    Service.objects.get_or_create(title=data['title'], defaults=data)
    print(f"Service '{data['title']}' created or retrieved.")
