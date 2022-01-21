<?xml version="1.0" encoding="UTF-8"?>
<tileset version="1.5" tiledversion="1.7.2" name="test" tilewidth="32" tileheight="32" tilecount="3" columns="0">
 <grid orientation="orthogonal" width="1" height="1"/>
 <tile id="3" type="grass">
  <image width="32" height="32" source="../sprites/1.png"/>
 </tile>
 <tile id="4" type="wall">
  <image width="32" height="32" source="../sprites/2.png"/>
  <objectgroup draworder="index" id="2">
   <object id="2" x="15.2881" y="15.9601"/>
  </objectgroup>
 </tile>
 <tile id="5" type="water">
  <image width="32" height="32" source="../sprites/3.png"/>
  <animation>
   <frame tileid="3" duration="190"/>
   <frame tileid="4" duration="190"/>
   <frame tileid="5" duration="190"/>
  </animation>
 </tile>
</tileset>
