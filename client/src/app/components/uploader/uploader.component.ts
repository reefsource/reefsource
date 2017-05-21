import {Component, OnInit} from "@angular/core";
import {Observable} from "rxjs/Observable";
import {ActivatedRoute} from "@angular/router";
import {Store} from "@ngrx/store";
import * as fromRoot from "../../reducers";
import {Album} from "../../models/album";
import {FileUploader} from "ng2-file-upload";
import {CookieService} from "angular2-cookie/core";

@Component({
  selector: 'app-uploader',
  templateUrl: './uploader.component.html',
  styleUrls: ['./uploader.component.css']
})
export class UploaderComponent implements OnInit {

  public album$: Observable<Album>;
  private albumId: number;
  private selectedFiles: FileList;
  public uploader: FileUploader;


  constructor(private route: ActivatedRoute,
              private store: Store<fromRoot.State>,
              private _cookieService: CookieService) {

  }

  ngOnInit() {
    this.albumId = +this.route.params['value']['albumId'];
    this.uploader = new FileUploader({url: `/api/v1/albums/${this.albumId}/upload/`});
    this.uploader.setOptions({headers: [{name: 'X-CSRFToken', value: this._cookieService.get('csrftoken')}]});
  }

}
