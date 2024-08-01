import React from 'react';

interface ClothingItemsProps {
  items: { imageUrl: string; link: string }[];
}

const ClothingItems: React.FC<ClothingItemsProps> = ({ items }) => {
  return (
    <div>
      {items.map((item, index) => (
        <div key={index}>
          <img src={item.imageUrl} alt="Clothing Item" />
          <a href={item.link} target="_blank" rel="noopener noreferrer">
            View Item
          </a>
        </div>
      ))}
    </div>
  );
};

export default ClothingItems;
