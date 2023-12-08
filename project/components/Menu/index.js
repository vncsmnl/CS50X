// Componentes como o Botão meus links e o social media.

import { BsInstagram, BsPersonCircle, BsTwitter } from 'react-icons/bs'
import Link from 'next/link'
import { FiGithub } from 'react-icons/fi'

export default function Menu() {
    return (
        <div className='menu'>
            <a className='social' href="https://vinicius.is-a.dev/" target="_blank" rel="noopener noreferrer">
                <BsPersonCircle color='#fff' size={24} />
            </a>
            <a className='social' href="https://github.com/vncsmnl" target="_blank" rel="noopener noreferrer">
                <FiGithub color='#fff' size={24} />
            </a>
            <a className='social' href="https://instagram.com/vncsmnl" target="_blank" rel="noopener noreferrer">
                <BsInstagram color='#fff' size={24} />
            </a>
            <a className='social' href="https://twitter.com/vncsmnl" target="_blank" rel="noopener noreferrer">
                <BsTwitter color='#fff' size={24} />
            </a>
            <div className='menu-item'>
                <Link href="./Links" passHref>
                    <p>Meus Links</p>
                </Link>
            </div>
        </div>
    )
}