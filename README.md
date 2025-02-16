# StyleAgent 🎭

StyleAgent is an AI-powered fashion recommendation system that helps users discover products matching their personal style based on their existing wardrobe.

## Inspiration 💡

The fashion industry has always been about personal expression, but finding products that match your unique style can be overwhelming. We wanted to create a tool that understands your fashion preferences through your existing outfits and helps you discover new pieces that complement your style. The idea came from the frustration of spending hours browsing through online stores trying to find items that match our aesthetic.

## What it does 🚀

StyleAgent allows users to:
- Upload photos of their favorite outfits
- Get AI-powered analysis of their personal style profile
- Receive curated outfit recommendations based on their style
- Discover shoppable products that match their aesthetic
- View detailed product information including prices and direct purchase links

## How we built it 🛠️

StyleAgent is built with a modern tech stack:

Frontend:
- Next.js 13 with App Router for the web interface
- Shadcn/UI for beautiful, accessible components
- TailwindCSS for styling
- React Dropzone for image uploads

Backend:
- FastAPI for the Python backend server
- OpenAI's GPT-4o-mini for style analysis
- DALL-E 3 for outfit visualization
- SerpAPI for product recommendations
- Python for image processing and API integrations

## Challenges we ran into 🤔

1. Style Analysis: Creating accurate style profiles from limited image data
2. Product Matching: Finding the right balance between style similarity and product availability
3. Performance: Optimizing API calls to maintain fast response times
4. UI/UX: Creating an intuitive interface for uploading and viewing multiple images

## Accomplishments that we're proud of 🏆

1. Created a seamless user experience from upload to recommendation
2. Implemented sophisticated AI analysis of personal style
4. Achieved high accuracy in style matching and recommendations

## What we learned 📚

- Working with multiple AI models in production
- Building efficient image processing pipelines
- Implementing real-time product search and filtering
- Managing complex state in a modern React application
- Handling large-scale data processing in FastAPI

## What's next for StyleAgent 🔮

1. Virtual Wardrobe: Allow users to save and organize their outfits
2. Style Evolution: Track how user's style changes over time
3. Social Features: Share outfits and recommendations with friends
4. Brand Integration (Ads): Direct partnerships with fashion retailers
5. Mobile App: Native mobile experience for easier photo capture

## Getting Started 🚀

1. Clone the repository
```bash
git clone https://github.com/yourusername/styleagent.git
cd styleagent
```

2. Set up the backend
```bash
cd server
pip install -r requirements.txt
# Add your API keys to .env file
fastapi dev main.py
```

3. Set up the frontend
```bash
cd client
pnpm install
pnpm dev
```

4. Open http://localhost:3000 in your browser

## Environment Variables 🔑

Create a `.env` file in the server directory with:
```
OPENAI_API_KEY=your_openai_api_key
SERPAPI_KEY=your_serpapi_key
```

## Contributing 🤝

We welcome contributions! Please feel free to submit a Pull Request. 