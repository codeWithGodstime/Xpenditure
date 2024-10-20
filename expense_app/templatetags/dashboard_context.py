from django import template

register = template.Library()
# https://cdn-icons-png.flaticon.com/128/2626/2626269.png
data = [
    {
        "imageUrl": "https://images.ctfassets.net/y2ske730sjqp/5QQ9SVIdc1tmkqrtFnG9U1/de758bba0f65dcc1c6bc1f31f161003d/BrandAssets_Logos_02-NSymbol.jpg",
        "name": "Netflix"
    },
    {
        "imageUrl": "https://cdn-icons-png.flaticon.com/128/3669/3669986.png",
        "name": "Spotify"
    },
    {
        "imageUrl": "https://cdn-icons-png.flaticon.com/128/15466/15466027.png",
        "name": "Amazon"
    },
    {
        "imageUrl": "https://cdn-icons-png.flaticon.com/128/300/300221.png",
        "name": "google"
    }
]

@register.simple_tag()
def fixed_expenses():
    return data