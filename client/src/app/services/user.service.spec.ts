/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { UserService } from './user.service';
import { HttpModule, Http, BaseRequestOptions, Response, ResponseOptions } from '@angular/http';
import { MockBackend } from '@angular/http/testing';

describe('TransactionService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpModule],
      providers: [
        UserService,
        {
          provide: Http,
          useFactory: (mockBackend, options) => {
            return new Http(mockBackend, options);
          },
          deps: [MockBackend, BaseRequestOptions]
        },
        MockBackend,
        BaseRequestOptions,
      ]
    });
  });

  it('should create the service', inject([UserService], (service: UserService) => {
    expect(service).toBeTruthy();
  }));

  it('should GET all the users',
  inject([UserService, MockBackend], (service: UserService, mockBackend: MockBackend) => {
    const mockResponse = [{
      'url': 'http://localhost:8000/api/users/2/',
      'username': 'nir',
      'email': '',
      'groups': []
    }, {
      'url': 'http://localhost:8000/api/users/1/',
      'username': 'admin',
      'email': 'admin@example.com',
      'groups': []
    }];

    mockBackend.connections.subscribe((connection) => {
      connection.mockRespond(new Response(new ResponseOptions({
        body: JSON.stringify(mockResponse)
      })));
    });

    service.getProfile().subscribe(user => {
      expect(user.username).toEqual('nir');
      expect(user.url).toEqual('http://localhost:8000/api/users/2/');
      expect(user.username).toEqual('admin');
      expect(user.email).toEqual('admin@example.com');
    });
  }));

});
