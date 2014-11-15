//
//  HPServiceManager.m
//  hplus
//
//  Created by aseem on 11/14/14.
//  Copyright (c) 2014 Aseem. All rights reserved.
//

#import "HPServiceManager.h"
#import "HPServiceCommunicator.h"
#import "HPStoryBuilder.h"
#import "HPServiceManagerDelegate.h"

@implementation HPServiceManager

- (void) fetchStories
{
    [self.communicator getHPStories];
}

#pragma mark - HPServiceCommunicatorDelegate

- (void) receivedStoriesJSON:(NSData *)data
{
    NSError *error = nil;
    NSArray *stories = [HPStoryBuilder storiesFromJSON:data
                                                error:&error];
    
    if (error == nil)
    {
        [self.delegate didReceiveStories:stories];
    }
    else
    {
        [self.delegate fetchingStoriesFailedWithError:error];
    }
}

- (void) fetchingStoriesFailedWithError:(NSError *)error
{
    [self.delegate fetchingStoriesFailedWithError:error];
}

@end
