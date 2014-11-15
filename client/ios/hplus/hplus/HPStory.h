//
//  HPStory.h
//  hplus
//
//  Created by aseem on 11/14/14.
//  Copyright (c) 2014 Aseem. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface HPStory : NSObject
@property (strong, nonatomic) NSString *author;
@property (strong, nonatomic) NSString *rank;
@property (strong, nonatomic) NSString *score;
@property (strong, nonatomic) NSString *time;
@property (strong, nonatomic) NSString *url;
@property (nonatomic) NSUInteger storyID;
@end
