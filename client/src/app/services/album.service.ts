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
}
