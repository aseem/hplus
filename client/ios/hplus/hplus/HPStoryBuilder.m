//
//  HPStoryBuilder.m
//  hplus
//
//  Created by aseem on 11/14/14.
//  Copyright (c) 2014 Aseem. All rights reserved.
//

#import "HPStoryBuilder.h"
#import "HPStory.h"

@implementation HPStoryBuilder


+ (NSArray *)storiesFromJSON:(NSData *)data error:(NSError *__autoreleasing *)error
{
    NSError *localError = nil;
    NSArray *parsedObject = [NSJSONSerialization JSONObjectWithData:data
                                                                 options:0
                                                                   error:&localError];
    
    if (localError != nil) {
        *error = localError;
        return nil;
    }
    
    NSMutableArray *stories = [[NSMutableArray alloc] init];
    for (NSDictionary *storyDict in parsedObject)
    {
        HPStory *story = [[HPStory alloc] init];
        story.author = [storyDict objectForKey:@"by"];
        story.rank = [storyDict objectForKey:@"rank"];
        story.score = [storyDict objectForKey:@"score"];
        story.time = [storyDict objectForKey:@"time"];
        story.url = [storyDict objectForKey:@"url"];
        story.storyID = [[storyDict objectForKey:@"id"] integerValue];
        
        [stories addObject:story];
    }
    
    return stories;
}

@end
