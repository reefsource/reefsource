import {Component, OnInit} from '@angular/core';
import {Album} from '../../models/album';
import {AlbumService} from '../../services/album.service';
import {MdDialogRef} from '@angular/material';

@Component({
  selector: 'app-album-new',
  templateUrl: './album-new.component.html',
  styleUrls: ['./album-new.component.css']
})
export class AlbumNewComponent implements OnInit {

  album: Album = {
    name: '',
    lat: 37,
    lng: -122,
    date: new Date(),
  };

  map = {
    zoom: 6,
    lat: 0,
    lng: 0
  };

  constructor(private dialog: MdDialogRef<AlbumNewComponent>, private albumService: AlbumService) {
  }

  ngOnInit() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(this.setMapCenterPosition.bind(this));
    }
  }

  setMapCenterPosition(position) {
    this.map.lat = this.album.lat = position.coords.latitude;
    this.map.lng = this.album.lng = position.coords.longitude;
  }

  mapClicked($event) {
    this.album.lat = $event.coords.lat;
    this.album.lng = $event.coords.lng;
  }

  markerDragEnd($event: MouseEvent) {
    this.mapClicked($event);
  }

  createAlbum() {
    this.albumService.createAlbum(this.album)
      .subscribe((response) => {
        this.dialog.close();
      });
  }
}
