//
//  HPServiceCommunicator.m
//  hplus
//
//  Created by aseem on 11/14/14.
//  Copyright (c) 2014 Aseem. All rights reserved.
//

#import "HPServiceCommunicator.h"
#import "HPServiceCommunicatorDelegate.h"

@implementation HPServiceCommunicator

- (void) getHPStories
{
    // Create the request
    NSURL *url= [NSURL URLWithString:@"http://54.243.48.46/api/1.0/hn"];
    
    [NSURLConnection sendAsynchronousRequest:[[NSURLRequest alloc] initWithURL:url] queue:[[NSOperationQueue alloc] init]
                           completionHandler:^(NSURLResponse *response, NSData *data, NSError *error)
     {
         if (error)
             [self.delegate fetchingStoriesFailedWithError:error];
         else
             [self.delegate receivedStoriesJSON:data];
     }];
}

@end
