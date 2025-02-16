import os
from openai import OpenAI
from typing import List, Dict, Any


def generateOutfits(profile: Dict[str, Any], num_outfits: int = 5) -> List[str]:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def generateOutfitDescriptions(
        profile: Dict[str, Any], num_outfits: int = 5
    ) -> List[str]:
        """
        Generate outfit descriptions based on a user profile.
        Returns a list of string descriptions for outfits.
        """
        system_prompt = """Given a customer profile, generate {num_outfits} unique outfit descriptions.
        Each description should be 1-2 sentences that describe the type of outfit and its purpose.
        Consider the person's age, style preferences, and influences.
        Focus on creating a range from casual to more dressed up while staying true to their aesthetic.
        Return just the descriptions as a Python list of strings, no additional formatting."""

        try:
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": f"Profile:\n{str(profile)}\n\nGenerate {num_outfits} outfit descriptions.",
                    },
                ],
                max_tokens=500,
            )

            # Parse the response into a list
            outfit_descriptions = eval(response.choices[0].message.content)

            if (
                not isinstance(outfit_descriptions, list)
                or len(outfit_descriptions) != num_outfits
            ):
                raise ValueError("Invalid response format for outfit descriptions")

            return outfit_descriptions
        except Exception as e:
            raise Exception(f"Error generating outfit descriptions: {str(e)}")

    # Generate the outfit descriptions
    outfit_descriptions = generateOutfitDescriptions(profile, num_outfits)

    # Create a detailed prompt based on the profile
    base_prompt = f"""
    Create a diverse outfit for someone with these characteristics:
    - Age: {profile["Age"]}
    - Style: {profile["Attire Style"]}
    - Style Archetype: {profile["Style Archetype"]}
    - Color Palette: {profile["Color Palette"]}
    - Influences: {profile["Influence"]}
    
    The outfit should be a full-body shot on a plain background, photorealistic, high quality fashion photography style.
    Show the complete outfit including accessories. No human in the image, just the clothing arranged.
    """

    generated_images = []

    try:
        for description in outfit_descriptions[:num_outfits]:
            prompt = f"{base_prompt}\nSpecifically: {description}"

            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )

            generated_images.append(response.data[0].url)

        return {
            "outfit_recommendations": [
                {"url": url, "description": description}
                for url, description in zip(
                    generated_images, outfit_descriptions[:num_outfits]
                )
            ]
        }

    except Exception as e:
        raise Exception(f"Error generating outfits: {str(e)}")
