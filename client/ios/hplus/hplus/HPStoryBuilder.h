//
//  HPStoryBuilder.h
//  hplus
//
//  Created by aseem on 11/14/14.
//  Copyright (c) 2014 Aseem. All rights reserved.
//

#import <Foundation/Foundation.h>

@interface HPStoryBuilder : NSObject

+ (NSArray *)storiesFromJSON:(NSData *)data error:(NSError **)error;

@end
