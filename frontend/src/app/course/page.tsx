import { Home } from 'lucide-react'
import Link from 'next/link'
import { Button } from '~/src/components/ui/button'
 
export default function NoCourseID() {
  return (
    <div className='text-center'>
      <h2 className='text-2xl'><b>No course ID given.</b></h2>
      <Button asChild className='m-4'>
        <Link href='/'>
          <Home className='mr-2 size-4' />
          Back to home
        </Link>
      </Button>
    </div>
  )
}