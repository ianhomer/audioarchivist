function audio_conversion_test
  echo "Audio Conversion Test"
  set in $argv
  set name (echo $in | cut -d'.' -f1 | cut -d'-' -f1)
  set name (string trim -- $name)
  echo "Converting audio : $name"
  ffmpeg -hide_banner -i $in
  mkdir $name
  for conversion in ogg-1 ogg-5 ogg-10 mp3-32 mp3-64 mp3-128 mp3-256 m4a-32 m4a-64 m4a-128 m4a-256 
    echo "Conversion : $conversion"
    set parts (string split '-' "$conversion")
    set ext $parts[1]
    echo "... extension : $ext"
    echo "... ... converting $out"
    set ffmpegArg -hide_banner -metadata artist=Me -metadata album=Test
    for ac in 1 2
      switch $ac
      case 1
        set channels Mono
      case '*'
        set channels Stereo
      end
      set ffmpegArg $ffmpegArg -ac $ac
      switch $ext
      case ogg
        set quality $parts[2]
        set ffmpegArg $ffmpegArg -qscale:a $quality
        set variation $channels q$quality
      case '*'
        set bitRate $parts[2]k
        set ffmpegArg $ffmpegArg -b:a $bitRate
        set variation $channels $bitRate
      end
      set out "$name/$name - $variation.$ext"
      set ffmpegArg $ffmpegArg -metadata title="$name - $variation"
      if test ! -f $out
        echo $out
        echo $ffmpegArg
        ffmpeg -hide_banner -i $in $ffmpegArg $out
      end
      ffmpeg -hide_banner -i $out
    end
  end  
end
