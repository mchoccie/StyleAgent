"use client"

import { useState } from "react"
import { ImageUpload } from "@/components/ui/image-upload"
import { ProductGrid } from "@/components/ui/product-grid"
import { Button } from "@/components/ui/button"
import { Loader2 } from "lucide-react"

interface Product {
  name: string
  link: string
  price: string | number
  image: string
  source: string
  thumbnail: string
}

export default function Home() {
  const [files, setFiles] = useState<File[]>([])
  const [products, setProducts] = useState<Product[]>([])
  const [isLoading, setIsLoading] = useState(false)

  const handleGenerate = async () => {
    if (!files.length) return

    setIsLoading(true)
    try {
      const formData = new FormData()
      files.forEach((file) => {
        formData.append("images", file)
      })

      const response = await fetch("http://localhost:8000/generate", {
        method: "POST",
        body: formData,
      })

      if (!response.ok) {
        throw new Error("Failed to generate products")
      }

      const data = await response.json()
      setProducts(data.items || [])
    } catch (error) {
      console.error("Error generating products:", error)
    } finally {
      setIsLoading(false)
    }
  }

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
            disabled={!files.length || isLoading}
          >
            {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
            Generate Products
          </Button>
        </div>

        <ProductGrid products={products} isLoading={isLoading} />
      </div>
    </main>
  )
}
