//
//  HPServiceCommunicator.h
//  hplus
//
//  Created by aseem on 11/14/14.
//  Copyright (c) 2014 Aseem. All rights reserved.
//

#import <Foundation/Foundation.h>

@protocol HPServiceCommunicatorDelegate;

@interface HPServiceCommunicator : NSObject

@property (weak, nonatomic) id<HPServiceCommunicatorDelegate> delegate;
-(void) getHPStories;

@end
