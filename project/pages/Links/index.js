// Pagina com os meus Links
import { useState, useEffect } from 'react';
import { FiLink, FiArrowLeft, FiTrash} from 'react-icons/fi'
import Link from 'next/link'
import Modal from '../../components/Modal';

import { getLinksSave, deleteLink} from '../../services/storeLinks';

export default function Links(){
  const [myLinks, setMyLinks] = useState([]);

  const [data, setData] = useState({});
  const [showModal, setShowModal] = useState(false);

  const [emptyList, setEmptyList] = useState(false);

  useEffect(() => {
    async function getLinks(){
      const result = await getLinksSave('@encurtaLink')

      if(result.length === 0){
        //nossa lista esta vazia...
        setEmptyList(true);
      }

      setMyLinks(result);
    }

    getLinks();
  }, [])

  function handleOpenLink(link){
    setData(link);
    setShowModal(true);
  }

  async function handleDelete(id){
    const result = await deleteLink(myLinks, id)

    if(result.length === 0){
      setEmptyList(true)
    }

    setMyLinks(result)

  }

  return(
    <div className='links-container'>

      <div className='links-header'>
        <Link href="/" passHref> 
        <FiArrowLeft size={40} color='#FFF'/>
        </Link>
        <h1>Meus Links</h1>
      </div>

      {emptyList && (
        <div className="links-item"> 
        <h2 className="empty-text">
          Sua lista está vazia!
        </h2>
        </div>
      )}

      {myLinks.map( link => (
      // eslint-disable-next-line react/jsx-key
        <div key={link.id} className='links-item'>
          <button className='link' onClick={ () => handleOpenLink(link)}>
            <FiLink size={18} color='#FFF'/>
              {link.long_url}
          </button>
          <button className='link-delete' onClick={() => handleDelete(link.id)}>
            <FiTrash size={24} color='red'/>
          </button>
      </div>
      ))}

      {showModal && (
      <Modal
        closeModal={() => setShowModal(false)}
        content={data}
      />
    )}

    </div>
  )
}