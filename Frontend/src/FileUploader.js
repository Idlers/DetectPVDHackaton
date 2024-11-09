import React, { useState } from 'react';
import './FileUploader.css'; // Импорт CSS файла
import logo from './logo.png'; // Импортируем логотип

const FileUploader = () => {
  const [file, setFile] = useState(null);
  const [fileName, setFileName] = useState('');
  const [error, setError] = useState('');
  const [reportGenerated, setReportGenerated] = useState(false);
  const [showReportButton, setShowReportButton] = useState(false);
  const [reportData, setReportData] = useState([]); // Изменено на массив

  const handleFileChange = (event) => {
    const selectedFile = event.target.files[0];
    const validFileTypes = ['video/mp4', 'video/avi', 'video/mkv', 'image/jpeg', 'image/png', 'image/gif'];

    if (selectedFile) {
      console.log("Файл загружен:", selectedFile.type);
      if (!validFileTypes.includes(selectedFile.type)) {
        setError('Файл не подходит. Пожалуйста, загрузите видео или изображение.');
        setFile(null);
        setFileName('');
      } else {
        setError('');
        setFile(selectedFile);
        setFileName(selectedFile.name);
      }
    } else {
      setFile(null);
      setFileName('');
    }
  };

  const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('video', file); // Use 'video' as the key to match your backend
    try {
      const response = await fetch('http://localhost:8000/api/violations/', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        const data = await response.json(); // Получаем массив данных
        alert(`Файл ${fileName} успешно отправлен!`);

        setReportData(data); // Теперь это массив объектов данных
        setShowReportButton(true);
      } else {
        const errorData = await response.json();
        setError(`Ошибка: ${errorData.error || 'Неизвестная ошибка'}`);
        setShowReportButton(false);
      }
    } catch (error) {
      console.error('Ошибка:', error);
      setError('Ошибка при отправке файла. Проверьте консоль для получения дополнительной информации.');
      setShowReportButton(false);
    }
  };

  const handleReportGeneration = () => {
    setReportGenerated(true);
  };

  return (
    <div className="container">
      <div className="logo-container">
        <img src={logo} alt="Логотип" className="logo" />
      </div>
      <div className="square">
        <h1 className="title">{fileName ? fileName : 'Ваше видео или фото'}</h1>
        <input 
          type="file" 
          accept="video/*,image/*" 
          onChange={handleFileChange} 
          className="input" 
        />
        {error && <p className="error">{error}</p>}
      </div>
     
      {file && (
        <button onClick={handleSubmit} className="submit-button">
          Отправить видео или фото
        </button>
      )}

      {showReportButton && !reportGenerated && (
        <button onClick={handleReportGeneration} className="report-button">
          Сформировать отчет
        </button>
      )}

      {reportGenerated && reportData.length > 0 && ( // Проверяем, что есть элементы в массиве
        <div className="modal">
          <div className="modal-content">
            <button onClick={() => setReportGenerated(false)} className="exit-button">
              Выход
            </button>
            <h2>Отчет о нарушениях</h2>
            <div className="scrollable"> {/* Применяем стиль для прокрутки */}
              <table className="report-table">
                <thead>
                  <tr>
                    <th>Статья нарушения</th>
                    <th>Время нарушения</th>
                    <th>Размер штрафа</th>
                  </tr>
                </thead>
                <tbody>
                  {reportData.map((report) => ( // Итерация по массиву reportData
                    <tr key={report.id}>
                      <td>{report.violation_article}</td>
                      <td>{report.violation_time} сек</td>
                      <td>{report.fine_amount} ₽</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default FileUploader;


