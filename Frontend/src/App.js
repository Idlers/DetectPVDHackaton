import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import FileUploader from './FileUploader'; // Make sure it points to the correct path
 // Create this component to handle results

const App = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<FileUploader />} />
        
      </Routes>
    </Router>
  );
};

export default App;
