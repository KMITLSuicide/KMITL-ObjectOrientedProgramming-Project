import { Lusitana } from 'next/font/google';
import localFont from 'next/font/local';

export const inter = localFont({
  src: [
    { path: './inter-variable/InterVariable.woff2', style: 'normal' },
    { path: './inter-variable/InterVariable-Italic.woff2', style: 'italic' },
  ],
});
export const lusitana = Lusitana({ weight: '400', subsets: ['latin'] });
