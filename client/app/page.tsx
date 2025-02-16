"use client";

import { useState } from "react";
import { ImageUpload } from "@/components/ui/image-upload";
import { ProductGrid } from "@/components/ui/product-grid";
import { Button } from "@/components/ui/button";
import { Loader2 } from "lucide-react";
import Image from "next/image";
import { useEffect } from "react";

interface Product {
  name: string;
  link: string;
  price: string | number;
  image: string;
  source: string;
  thumbnail: string;
}

interface OutfitRecommendation {
  url: string;
  description: string;
}

interface Profile {
  Age: number;
  Occupation: string;
  Location: string;
  Hobbies: string[];
  Ethnicity: string;
  "Attire Style": string;
  "Style Archetype": string;
  "Color Palette": string;
  Influence: string;
}

interface MessageEvent {
  data: string;
}

export default function Home() {
  const [files, setFiles] = useState<File[]>([]);
  const [products, setProducts] = useState<Product[]>([]);
  const [outfits, setOutfits] = useState<OutfitRecommendation[]>([]);
  const [isLoading, setIsLoading] = useState(false);
  const [isGeneratingOutfits, setIsGeneratingOutfits] = useState(false);
  const [isGeneratingProducts, setIsGeneratingProducts] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleGenerate = async () => {
    if (!files.length) return;

    setIsLoading(true);
    setOutfits([]);
    setProducts([]);
    setError(null);

    try {
      // First, upload images and get profile
      const formData = new FormData();
      files.forEach((file) => {
        formData.append("images", file);
      });

      const profileResponse = await fetch("http://localhost:8000/generate", {
        method: "POST",
        body: formData,
      });

      if (!profileResponse.ok) {
        throw new Error("Failed to generate profile");
      }

      const profileData = await profileResponse.json();
      setIsLoading(false);
      setIsGeneratingOutfits(true);

      // Start streaming outfit generations
      const eventSource = new EventSource(
        `http://localhost:8000/generate-outfits?profile=${encodeURIComponent(
          JSON.stringify(profileData.profile)
        )}`
      );

      eventSource.addEventListener("outfit", (event: MessageEvent) => {
        const outfit = JSON.parse(event.data);
        setOutfits((prev) => [...prev, outfit]);
      });

      eventSource.addEventListener("error", (event: MessageEvent) => {
        const error = JSON.parse(event.data);
        setError(error.message || "An error occurred while generating outfits");
        eventSource.close();
        setIsGeneratingOutfits(false);
      });

      eventSource.addEventListener("complete", async (event: MessageEvent) => {
        eventSource.close();
        setIsGeneratingOutfits(false);
        setIsGeneratingProducts(true);

        // After outfits are complete, get product recommendations
        try {
          const productsResponse = await fetch(
            "http://localhost:8000/generate-items",
            {
              method: "GET",
            }
          );

          if (!productsResponse.ok) {
            throw new Error("Failed to generate products");
          }

          const productsData = await productsResponse.json();
          setProducts(productsData || []);
        } catch (error) {
          setError("Failed to generate product recommendations");
        } finally {
          setIsGeneratingProducts(false);
        }
      });
    } catch (error) {
      setError("An error occurred while processing your request");
      setIsLoading(false);
      setIsGeneratingOutfits(false);
      setIsGeneratingProducts(false);
    }
  };

  return (
    <main className="container mx-auto py-8 px-4">
      <div className="max-w-4xl mx-auto space-y-8">
        <div className="text-center space-y-2">
          <h1 className="text-3xl font-bold">Style Agent</h1>
          <p className="text-muted-foreground">
            Upload your outfit photos and discover similar products you'll love
          </p>
        </div>

        <ImageUpload onImagesChange={setFiles} />

        <div className="flex justify-center">
          <Button
            size="lg"
            onClick={handleGenerate}
            disabled={
              !files.length ||
              isLoading ||
              isGeneratingOutfits ||
              isGeneratingProducts
            }>
            {(isLoading || isGeneratingOutfits || isGeneratingProducts) && (
              <Loader2 className="mr-2 h-4 w-4 animate-spin" />
            )}
            {isLoading
              ? "Analyzing Your Style..."
              : isGeneratingOutfits
              ? "Generating Outfits..."
              : isGeneratingProducts
              ? "Finding Products..."
              : "Generate Recommendations"}
          </Button>
        </div>

        {error && <div className="text-center text-red-500 py-4">{error}</div>}

        {outfits.length > 0 && (
          <div className="space-y-6">
            <h2 className="text-2xl font-semibold text-center">
              Outfits We Think You'd Love
              {isGeneratingOutfits && (
                <span className="text-sm font-normal text-muted-foreground ml-2">
                  (Generating more...)
                </span>
              )}
            </h2>
            <div className="grid grid-cols-2 md:grid-cols-3 gap-6">
              {outfits.map((outfit, index) => (
                <div key={index} className="space-y-2 animate-fadeIn">
                  <div className="relative aspect-square">
                    <Image
                      src={outfit.url}
                      alt={outfit.description}
                      fill
                      className="object-cover rounded-lg"
                    />
                  </div>
                  {/* <p className="text-sm text-muted-foreground">
                    {outfit.description}
                  </p> */}
                </div>
              ))}
            </div>
          </div>
        )}

        {isGeneratingProducts && (
          <div className="text-center py-8">
            <Loader2 className="w-8 h-8 animate-spin mx-auto mb-4" />
            <p className="text-muted-foreground">
              Finding matching products for you...
            </p>
          </div>
        )}

        {products.length > 0 && (
          <div className="space-y-6">
            <h2 className="text-2xl font-semibold text-center">
              Shop Similar Items
            </h2>
            <ProductGrid products={products} />
          </div>
        )}
      </div>
    </main>
  );
}

// Add this to your global CSS or create a new animation
// tailwind.config.js:
// extend: {
//   keyframes: {
//     fadeIn: {
//       '0%': { opacity: '0', transform: 'translateY(10px)' },
//       '100%': { opacity: '1', transform: 'translateY(0)' }
//     }
//   },
//   animation: {
//     fadeIn: 'fadeIn 0.5s ease-out forwards'
//   }
// }
