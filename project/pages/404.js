/* eslint-disable @next/next/no-img-element */
// Pagina 404 Customizada

import Link from 'next/link'
import Menu from '../components/Menu'

export default function FourOhFour() {
  return (
    <>

      <div className='Error404'>
        <img src="/public/404.svg" alt="Error 404" />
        <Link href="/">
          <a>
            <p>Volte para a Home</p>
          </a>
        </Link>
      </div>

      <Menu>
      </Menu>

    </>

  )
}
