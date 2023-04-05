<?php

$files = scandir('.');

array_shift($files);
array_shift($files);

print_r($files);

$sizes = [16,32,48,64];

// foreach($files as $file){
//     if(substr($file,strlen($file)-3,3) == 'png'){
//         $name = substr($file,0,strlen($file)-4);
//         foreach($sizes as $size){
//             exec("convert -resize {$size}x{$size} {$file}  {$name}_{$size}x{$size}.png");
//         }

//     }
// }

foreach($sizes as $size){
    exec("convert -resize {$size}x{$size} football.png  football_{$size}x{$size}.png");
}