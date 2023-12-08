/* eslint-disable @next/next/no-img-element */
// Pagina Home

import { useState } from 'react'
import { FiLink } from 'react-icons/fi'
import Menu from '../components/Menu'
import Modal from '../components/Modal';

import api from '../services/api';
import { saveLink } from '../services/storeLinks';

export default function Home() {
  const [link, setLink] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [data, setData] = useState({});



  async function handleShortLink() {
    try {
      const response = await api.post('/shorten', {
        long_url: link
      })

      setData(response.data);
      setShowModal(true);

      saveLink('@encurtaLink', response.data)

      setLink('');

    } catch {
      alert('URL Inválida')
      setLink('');
    }
  }

  return (
    <div className="container-home">

      <div className="logo">
        <img src="/home.svg" alt="home image" />
      </div>

      <div className="area-input">
        <div>
          <FiLink size={24} color='#FFF' />
          <input
            placeholder='Cole seu link aqui...'
            value={link}
            onChange={(event) => setLink(event.target.value)}
          />
        </div>
        <button onClick={handleShortLink}>Gerar Link!</button>
      </div>

      <Menu />

      {showModal && (
        <Modal
          closeModal={() => setShowModal(false)}
          content={data}
        />
      )}

      <footer className="footer"><img src="/footer.gif" width={150} alt="footer" /></footer>
    </div>
  )
}