const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

console.log('Compiling Tailwind CSS to public/tailwind.css and app/globals.css...');
execSync('npx tailwindcss -i ./styles/input.css -o ./public/tailwind.css --minify', { stdio: 'inherit' });
fs.copyFileSync(
  path.join(__dirname, 'public', 'tailwind.css'),
  path.join(__dirname, 'app', 'globals.css')
);
console.log('Tailwind CSS successfully built and mirrored.');
