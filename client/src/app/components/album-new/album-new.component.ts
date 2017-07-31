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
    lat: 0,
    lng: 0,
    date: new Date(),
  };

  map = {
    zoom: 3,
    lng: -99,
    lat: 40
  };

  constructor(private dialog: MdDialogRef<AlbumNewComponent>, private albumService: AlbumService) {
  }

  ngOnInit() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(this.setMapCenterPosition.bind(this));
    }
  }

  round(number, precision) {
    let factor = Math.pow(10, precision);
    let tempNumber = number * factor;
    let roundedTempNumber = Math.round(tempNumber);
    return roundedTempNumber / factor;
  };

  setMapCenterPosition(position) {
    this.map.lat = this.album.lat = position.coords.latitude;
    this.map.lng = this.album.lng = position.coords.longitude;
  }

  mapClicked($event) {
    this.album.lat = this.round($event.coords.lat, 4);
    this.album.lng = this.round($event.coords.lng,4);
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
