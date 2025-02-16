"use client"

import { useCallback, useState } from "react"
import { useDropzone } from "react-dropzone"
import { Card } from "./card"
import { Button } from "./button"
import Image from "next/image"
import { X } from "lucide-react"

interface ImageUploadProps {
  onImagesChange: (files: File[]) => void
}

export function ImageUpload({ onImagesChange }: ImageUploadProps) {
  const [files, setFiles] = useState<File[]>([])
  const [previews, setPreviews] = useState<string[]>([])

  const onDrop = useCallback((acceptedFiles: File[]) => {
    setFiles((prev) => [...prev, ...acceptedFiles])
    const newPreviews = acceptedFiles.map((file) => URL.createObjectURL(file))
    setPreviews((prev) => [...prev, ...newPreviews])
    onImagesChange([...files, ...acceptedFiles])
  }, [files, onImagesChange])

  const removeImage = (index: number) => {
    const newFiles = files.filter((_, i) => i !== index)
    const newPreviews = previews.filter((_, i) => i !== index)
    setFiles(newFiles)
    setPreviews(newPreviews)
    onImagesChange(newFiles)
  }

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'image/*': ['.jpeg', '.jpg', '.png']
    }
  })

  return (
    <div className="w-full space-y-4">
      <Card
        {...getRootProps()}
        className={`p-8 border-2 border-dashed cursor-pointer ${
          isDragActive ? "border-primary" : "border-muted-foreground"
        }`}
      >
        <input {...getInputProps()} />
        <div className="text-center">
          <p className="text-sm text-muted-foreground">
            {isDragActive
              ? "Drop the files here..."
              : "Drag & drop outfit images here, or click to select files"}
          </p>
        </div>
      </Card>

      {previews.length > 0 && (
        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4">
          {previews.map((preview, index) => (
            <div key={preview} className="relative group">
              <Image
                src={preview}
                alt={`Preview ${index + 1}`}
                width={200}
                height={200}
                className="rounded-lg object-cover w-full h-48"
              />
              <Button
                variant="destructive"
                size="icon"
                className="absolute top-2 right-2 opacity-0 group-hover:opacity-100 transition-opacity"
                onClick={() => removeImage(index)}
              >
                <X className="h-4 w-4" />
              </Button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
} 