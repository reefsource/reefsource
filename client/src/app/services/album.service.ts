import {Injectable} from "@angular/core";
import {Headers, Http, RequestOptions} from "@angular/http";
import {Observable} from "rxjs/Observable";
import {BaseService} from "./base.service";
import {Album} from "../models/album";

@Injectable()
export class AlbumService extends BaseService {

  constructor(private http: Http,) {
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

  uploadFile(albumId: number, fileList: FileList) {
    if (fileList.length > 0) {
      let file: File = fileList[0];

      let formData: FormData = new FormData();
      formData.append('uploadFile', file, file.name);

      let headers = new Headers();
      headers.append('Content-Type', 'multipart/form-data');
      headers.append('Accept', 'application/json');

      let options = new RequestOptions({headers: headers});

      return this.http.post(`/api/v1/albums/${albumId}/upload/`, formData, options)
        .map(res => res.json())
        .catch(this.handleError)
        .subscribe(
          data => console.log('success'),
          error => console.log(error)
        );
    }
  }
}
