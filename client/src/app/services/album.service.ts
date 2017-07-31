import 'rxjs/add/operator/map'
import 'rxjs/add/operator/catch'

import {Injectable} from '@angular/core';
import {Http} from '@angular/http';
import {Observable} from 'rxjs/Observable';
import {BaseService} from './base.service';
import {Album} from '../models/album';

@Injectable()
export class AlbumService extends BaseService {

  constructor(private http: Http) {
    super();
  }

  getAlbums(): Observable<Album[]> {
    return this.http.get('/api/v1/albums/')
      .map(res => res.json())
      .catch(this.handleError);
  }

  getAlbum(id: number): Observable<Album> {
    return this.http.get(`/api/v1/albums/${id}/`)
      .map(res => res.json())
      .catch(this.handleError);
  }

  createAlbum(album: Album): Observable<Album> {
    const decimals = 1000000;
    album.lat = Math.round(album.lat * decimals) / decimals;
    album.lng = Math.round(album.lng * decimals) / decimals;

    return this.http.post(`/api/v1/albums/`, JSON.stringify(album), this.getOptions())
      .map(res => res.json())
      .catch(this.handleError);
  }

  deleteAlbum(albumId: number): Observable<any> {
    return this.http.delete(`/api/v1/albums/${albumId}/`, this.getOptions())
      .map(res => res.json())
      .catch(this.handleError);
  }
}
