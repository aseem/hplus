//
//  HPServiceManagerDelegate.h
//  hplus
//
//  Created by aseem on 11/14/14.
//  Copyright (c) 2014 Aseem. All rights reserved.
//

#import <Foundation/Foundation.h>

@protocol HPServiceManagerDelegate <NSObject>

- (void) didReceiveStories:(NSArray *)stories;
- (void) fetchingStoriesFailedWithError:(NSError *)error;

@end
