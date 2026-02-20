import React from 'react';
import { ProfileContainer, ProfileHeader, ProfileSections } from './Profile.styles';
import { ProfileProps } from './Profile.types';
import { Avatar } from '../../design-system/components/Avatar';
import { ProfileStats, ProfileSettings } from './Profile.sections';

export const Profile: React.FC<ProfileProps> = () => {
  return (
    <ProfileContainer>
      <ProfileHeader>
        <Avatar name="User" size="xl" />
        <div>
          <h2>User Name</h2>
          <p>@username</p>
        </div>
      </ProfileHeader>
      <ProfileSections>
        <ProfileStats />
        <ProfileSettings />
      </ProfileSections>
    </ProfileContainer>
  );
};
