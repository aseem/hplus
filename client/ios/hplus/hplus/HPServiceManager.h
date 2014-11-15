//
//  HPServiceManager.h
//  hplus
//
//  Created by aseem on 11/14/14.
//  Copyright (c) 2014 Aseem. All rights reserved.
//

#import <Foundation/Foundation.h>
#import "HPServiceCommunicatorDelegate.h"

@protocol HPServiceManagerDelegate;

@class HPServiceCommunicator;

@interface HPServiceManager : NSObject<HPServiceCommunicatorDelegate>

@property (strong, nonatomic) HPServiceCommunicator *communicator;
@property (weak, nonatomic) id<HPServiceManagerDelegate> delegate;

- (void)fetchStories;

@end
