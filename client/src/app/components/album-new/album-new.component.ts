import {Component, OnInit} from '@angular/core';
import {Album} from '../../models/album';

@Component({
  selector: 'app-album-new',
  templateUrl: './album-new.component.html',
  styleUrls: ['./album-new.component.css']
})
export class AlbumNewComponent implements OnInit {

  album: Album = {
    name: '',
    lat: 37,
    long: -122,
    date: new Date(),
  };

  zoom = 3;

  constructor() {
  }

  ngOnInit() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(this.setPosition.bind(this));
    }
  }

  setPosition(position) {
    this.album.lat = position.coords.latitude;
    this.album.long = position.coords.longitude;
  }
}
