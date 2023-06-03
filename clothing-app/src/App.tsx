import React, { useState } from 'react';
import UploadForm from './pages/UploadForm';
import ClothingItems from './pages/ClothingItems';
import axios from 'axios';

interface ClothingItem {
  imageUrl: string;
  link: string;
}

const App: React.FC = () => {
  const [clothingItems, setClothingItems] = useState<ClothingItem[]>([]);

  const handleImageUpload = (file: File) => {
    // Perform upload logic and fetch similar clothing items
    // You can make an API call to your backend server and retrieve the similar items

    const reader = new FileReader();

    reader.onload = async () => {
    const imageData = new Uint8Array(reader.result as ArrayBuffer);

    try {
        const response = await axios.post('/api/images/similar', imageData, {
        headers: {
            'Content-Type': 'application/octet-stream',
        },
        });

        setClothingItems(response.data);
    } catch (error) {
        console.error('Error retrieving similar images:', error);
    }
    };

    reader.readAsArrayBuffer(file);

    // Mock response data for testing
    const mockItems: ClothingItem[] = [
      {
        imageUrl: 'https://example.com/item1.jpg',
        link: 'https://example.com/item1',
      },
      {
        imageUrl: 'https://example.com/item2.jpg',
        link: 'https://example.com/item2',
      },
    ];

    setClothingItems(mockItems);
  };

  return (
    <div>
      <h1>Clothing App</h1>
      <UploadForm onImageUpload={handleImageUpload} />
      {clothingItems.length > 0 && <ClothingItems items={clothingItems} />}
    </div>
  );
};

export default App;
