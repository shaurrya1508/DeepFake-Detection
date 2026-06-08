import { useState } from "react"
import axios from "axios"

function App() {

  const [image, setImage] = useState(null)
  const [selectedFile, setSelectedFile] = useState(null)
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)

  // =========================
  // IMAGE UPLOAD
  // =========================
  const handleImageUpload = (e) => {

    const file = e.target.files[0]

    if (file) {
      setSelectedFile(file)
      setImage(URL.createObjectURL(file))
    }
  }

  // =========================
  // ANALYZE IMAGE
  // =========================
  const analyzeImage = async () => {

    if (!selectedFile) return

    setLoading(true)

    const formData = new FormData()

    formData.append("image", selectedFile)

    try {

      const response = await axios.post(
        "http://127.0.0.1:5000/predict",
        formData
      )

      setResult(response.data)

    } catch (error) {

      console.error(error)
      alert("Error connecting to backend")

    }

    setLoading(false)
  }

  return (

    <div className="min-h-screen bg-gradient-to-br from-black via-gray-900 to-black text-white flex flex-col items-center justify-center px-4">

      {/* TITLE */}
      <h1 className="text-5xl md:text-6xl font-bold text-blue-500 mb-4">
        DeepFake Detector
      </h1>

      <p className="text-gray-400 mb-10 text-center max-w-xl">
        Upload an image and let AI analyze whether it is REAL or FAKE.
      </p>

      {/* CARD */}
      <div className="bg-white/10 backdrop-blur-lg border border-white/20 rounded-3xl p-8 w-full max-w-2xl shadow-2xl">

        {/* UPLOAD AREA */}
        <label className="border-2 border-dashed border-blue-500 rounded-2xl h-64 flex flex-col items-center justify-center cursor-pointer hover:bg-blue-500/10 transition">

          <input
            type="file"
            accept="image/*"
            className="hidden"
            onChange={handleImageUpload}
          />

          <p className="text-xl font-semibold text-blue-400">
            Click to Upload Image
          </p>

          <p className="text-gray-400 mt-2">
            JPG, PNG supported
          </p>

        </label>

        {/* IMAGE PREVIEW */}
        {image && (
          <div className="mt-8">

            <h2 className="text-xl font-semibold mb-4">
              Preview
            </h2>

            <img
              src={image}
              alt="preview"
              className="rounded-2xl w-full"
            />

            {/* ANALYZE BUTTON */}
            <button
              onClick={analyzeImage}
              className="mt-6 w-full bg-blue-600 hover:bg-blue-700 transition py-4 rounded-2xl text-lg font-bold"
            >

              {loading ? "Analyzing..." : "Analyze Image"}

            </button>

          </div>
        )}

        {/* RESULT */}
        {result && (
          <div className="mt-8 bg-black/40 p-6 rounded-2xl text-center">

            <h2 className="text-3xl font-bold mb-4">

              {result.prediction === "FAKE"
                ? "⚠️ FAKE"
                : "✅ REAL"}

            </h2>

            <p className="text-xl text-gray-300">
              Confidence: {result.confidence}%
            </p>

          </div>
        )}

      </div>

    </div>
  )
}

export default App