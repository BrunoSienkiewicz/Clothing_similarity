import React, { ChangeEvent, useState } from 'react';

interface UploadFormProps {
  onImageUpload: (file: File) => void;
}

const UploadForm: React.FC<UploadFormProps> = ({ onImageUpload }) => {

    const handleFileChange = (e: ChangeEvent<HTMLInputElement>) => {
        const file = e.target.files?.[0];
        if (file) {
        onImageUpload(file);
        }
    };

    return (
        <div>
        <input type="file" accept="image/*" onChange={handleFileChange} />
        </div>
    );
};

export default UploadForm;